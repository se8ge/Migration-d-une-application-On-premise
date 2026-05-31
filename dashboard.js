// État Global
let currentUser = null;
let allProducts = [];

const API_BASE = window.location.origin;

// --- Gestion des Vues ---
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute('data-section');
        
        // Update UI
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        document.getElementById(sectionId).classList.add('active');

        if(sectionId === 'inventory') refreshInventory();
        if(sectionId === 'dashboard') refreshStats();
        if(sectionId === 'suppliers') refreshSuppliers();
        if(sectionId === 'movements') refreshMovements();
    });
});

// --- Authentification ---
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');

    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (res.ok) {
            const data = await res.json();
            currentUser = data.user;
            localStorage.setItem('token', data.access_token);
            document.getElementById('login-overlay').style.display = 'none';
            refreshStats();
        } else {
            const errData = await res.json();
            errorEl.style.display = 'block';
            errorEl.innerText = errData.detail || "Identifiants incorrects";
        }
    } catch (err) {
        errorEl.style.display = 'block';
        errorEl.innerText = "Serveur inaccessible";
    }
});

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token');
    location.reload();
});

// --- Gestion de l'Inventaire ---
async function refreshInventory() {
    const body = document.getElementById('inventory-body');
    body.innerHTML = '<tr><td colspan="5" style="text-align:center">Chargement...</td></tr>';

    try {
        const res = await fetch(`${API_BASE}/products/`);
        if (res.ok) {
            allProducts = await res.json();
            body.innerHTML = '';
            allProducts.forEach(p => {
                const row = `
                    <tr>
                        <td><code>${p.product_code}</code></td>
                        <td>${p.product_name}</td>
                        <td>${p.retail_price} €</td>
                        <td>${p.min_stock}</td>
                        <td>
                            <div class="action-btns">
                                <button onclick="editProduct(${p.product_id})" class="icon-btn">✏️</button>
                                <button onclick="deleteProduct(${p.product_id})" class="icon-btn" style="color:var(--danger)">🗑️</button>
                            </div>
                        </td>
                    </tr>
                `;
                body.innerHTML += row;
            });
        }
    } catch (err) {
        body.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--danger)">Erreur de chargement</td></tr>';
    }
}

async function deleteProduct(id) {
    if (!confirm("Voulez-vous vraiment supprimer ce produit ?")) return;

    try {
        const res = await fetch(`${API_BASE}/products/${id}`, { method: 'DELETE' });
        if (res.ok) {
            alert("Produit supprimé !");
            refreshInventory();
            refreshStats();
        }
    } catch (err) {
        alert("Erreur lors de la suppression");
    }
}

// Formulaire Produit (Ajout / Edition)
document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('prod-id').value;
    const payload = {
        product_name: document.getElementById('prod-name').value,
        product_code: document.getElementById('prod-code').value,
        category: document.getElementById('prod-cat').value,
        purchase_price: parseFloat(document.getElementById('prod-price').value),
        retail_price: parseFloat(document.getElementById('prod-price').value) * 1.2, // Auto-calcul simple
        min_stock: parseInt(document.getElementById('prod-min').value),
        brand: "GEN",
        unit: "pcs",
        model: "M1",
        product_details: "Saisie manuelle",
        isactive: true
    };

    const url = id ? `${API_BASE}/products/${id}` : `${API_BASE}/products/`;
    const method = id ? 'PUT' : 'POST';

    try {
        // Pour le POST, on a besoin de createby
        if (!id) payload.createby = "admin";

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            hideModal('product-modal');
            refreshInventory();
            refreshStats();
            alert(id ? "Produit mis à jour !" : "Produit ajouté !");
        }
    } catch (err) {
        alert("Erreur lors de l'enregistrement");
    }
});

function editProduct(id) {
    const p = allProducts.find(prod => prod.product_id === id);
    if (!p) return;

    document.getElementById('modal-title').innerText = "Modifier le Produit";
    document.getElementById('prod-id').value = p.product_id;
    document.getElementById('prod-name').value = p.product_name;
    document.getElementById('prod-code').value = p.product_code;
    document.getElementById('prod-cat').value = p.category;
    document.getElementById('prod-price').value = p.purchase_price;
    document.getElementById('prod-min').value = p.min_stock;
    
    showModal('product-modal');
}

// --- Gestion des Fournisseurs ---
async function refreshSuppliers() {
    const body = document.getElementById('suppliers-body');
    body.innerHTML = '<tr><td colspan="5" style="text-align:center">Chargement...</td></tr>';

    try {
        const res = await fetch(`${API_BASE}/suppliers/`);
        if (res.ok) {
            const suppliers = await res.json();
            body.innerHTML = '';
            suppliers.forEach(s => {
                body.innerHTML += `
                    <tr>
                        <td><code>${s.supplier_code}</code></td>
                        <td>${s.supplier_name}</td>
                        <td>${s.contact_per_name}</td>
                        <td>${s.phone}</td>
                        <td style="text-align:right">
                            <button class="icon-btn">✏️</button>
                        </td>
                    </tr>
                `;
            });
        }
    } catch (err) {
        body.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--danger)">Erreur</td></tr>';
    }
}

document.getElementById('supplier-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        supplier_code: document.getElementById('supp-code').value,
        supplier_name: document.getElementById('supp-name').value,
        address: document.getElementById('supp-addr').value,
        phone: document.getElementById('supp-phone').value,
        email: document.getElementById('supp-email').value,
        contact_per_name: document.getElementById('supp-contact').value,
        c_p_contact: document.getElementById('supp-phone').value,
        createby: 1
    };

    try {
        const res = await fetch(`${API_BASE}/suppliers/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            hideModal('supplier-modal');
            refreshSuppliers();
            alert("Fournisseur ajouté !");
        }
    } catch (err) {
        alert("Erreur lors de l'ajout");
    }
});

// --- Gestion des Mouvements ---
async function refreshMovements() {
    const body = document.getElementById('movements-body');
    body.innerHTML = '<tr><td colspan="5" style="text-align:center">Chargement...</td></tr>';

    try {
        const res = await fetch(`${API_BASE}/stock/movements/`);
        if (res.ok) {
            const movements = await res.json();
            body.innerHTML = '';
            movements.forEach(m => {
                body.innerHTML += `
                    <tr>
                        <td><code>${m.proposal_code}</code></td>
                        <td>Magasin ${m.from_store_id}</td>
                        <td>Magasin ${m.for_store_id}</td>
                        <td>${m.proposal_datetime}</td>
                        <td><span class="badge ${m.is_approved ? 'badge-active' : 'badge-low'}">${m.is_approved ? 'Approuvé' : 'En attente'}</span></td>
                    </tr>
                `;
            });
        }
    } catch (err) {
        body.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--danger)">Erreur</td></tr>';
    }
}

document.getElementById('movement-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        proposal_code: "MOV-" + Date.now().toString().slice(-6),
        issue_code: null,
        for_store_id: parseInt(document.getElementById('move-to').value),
        from_store_id: parseInt(document.getElementById('move-from').value),
        proposal_datetime: new Date().toISOString().split('T')[0],
        proposal_by: 1,
        issue_datetime: new Date().toISOString().split('T')[0],
        issue_by: 1,
        is_approved: true,
        is_received: true,
        details: [
            {
                product_id: parseInt(document.getElementById('move-prod').value),
                received_qty: parseInt(document.getElementById('move-qty').value)
            }
        ]
    };

    try {
        const res = await fetch(`${API_BASE}/stock/movements/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            hideModal('movement-modal');
            refreshMovements();
            refreshStats();
            alert("Mouvement enregistré !");
        }
    } catch (err) {
        alert("Erreur lors du mouvement");
    }
});

// --- Animation compteur ---
function animateCounter(el, target, formatter) {
    const start = 0;
    const duration = 1200;
    const startTime = performance.now();
    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (target - start) * eased);
        el.innerText = formatter ? formatter(current) : current;
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// --- Statistiques & Alertes ---
async function refreshStats() {
    try {
        const [statsRes, alertsRes] = await Promise.all([
            fetch(`${API_BASE}/stats/`),
            fetch(`${API_BASE}/stock/alerts/`)
        ]);

        if (statsRes.ok) {
            const s = await statsRes.json();

            animateCounter(document.getElementById('stat-total'), s.total_products);
            animateCounter(document.getElementById('stat-alerts'), s.stock_alerts);
            animateCounter(document.getElementById('stat-movements'), s.movements_month);
            animateCounter(document.getElementById('stat-suppliers'), s.total_suppliers);
            animateCounter(document.getElementById('stat-items'), s.total_items_in_stock,
                v => v.toLocaleString('fr-FR'));
            animateCounter(document.getElementById('stat-value'), Math.round(s.stock_value),
                v => v.toLocaleString('fr-FR') + ' €');
        }

        if (alertsRes.ok) {
            const alerts = await alertsRes.json();
            const alertBody = document.getElementById('alert-body');
            alertBody.innerHTML = '';
            if (alerts.length === 0) {
                alertBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--text-muted); padding:2rem;">Aucune alerte — tous les stocks sont suffisants</td></tr>';
            } else {
                alerts.forEach(a => {
                    alertBody.innerHTML += `
                        <tr>
                            <td><strong>${a.product_name}</strong><br><span style="color:var(--text-muted);font-size:0.8rem">${a.product_code}</span></td>
                            <td style="color:var(--danger); font-weight:700;">Critique</td>
                            <td>${a.min_stock}</td>
                            <td><span class="badge badge-low">Réappro. urgente</span></td>
                        </tr>
                    `;
                });
            }
        }
    } catch (err) {
        console.error("Erreur Stats", err);
    }
}

// Rafraîchissement automatique toutes les 30 secondes
setInterval(() => {
    if (document.getElementById('login-overlay').style.display === 'none') {
        refreshStats();
    }
}, 30000);

// --- Modales ---
function showModal(id) {
    if (id === 'product-modal' && !document.getElementById('prod-id').value) {
        document.getElementById('product-form').reset();
        document.getElementById('prod-id').value = "";
        document.getElementById('modal-title').innerText = "Ajouter un Produit";
    }
    
    if (id === 'movement-modal') {
        const select = document.getElementById('move-prod');
        select.innerHTML = allProducts.map(p => `<option value="${p.product_id}">${p.product_name} (${p.product_code})</option>`).join('');
    }

    document.getElementById(id).style.display = 'flex';
}

function hideModal(id) {
    document.getElementById(id).style.display = 'none';
}

// Autoload
if (localStorage.getItem('token')) {
    // Dans une vraie app, on vérifierait le token ici
    document.getElementById('login-overlay').style.display = 'none';
    refreshStats();
}
