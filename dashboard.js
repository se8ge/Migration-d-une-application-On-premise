// État Global
let currentUser = null;
let allProducts = [];

const API_BASE = "http://localhost:8000";

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
            errorEl.style.display = 'block';
            errorEl.innerText = "Identifiants incorrects";
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

// --- Statistiques & Alertes ---
async function refreshStats() {
    try {
        const res = await fetch(`${API_BASE}/products/`);
        const resAlerts = await fetch(`${API_BASE}/stock/alerts/`);
        
        if (res.ok && resAlerts.ok) {
            const products = await res.json();
            const alerts = await resAlerts.json();

            document.getElementById('stat-total').innerText = products.length;
            document.getElementById('stat-alerts').innerText = alerts.length;
            
            const totalValue = products.reduce((acc, p) => acc + p.purchase_price, 0);
            document.getElementById('stat-value').innerText = `${totalValue.toFixed(2)} €`;

            const alertBody = document.getElementById('alert-body');
            alertBody.innerHTML = '';
            alerts.forEach(a => {
                alertBody.innerHTML += `
                    <tr>
                        <td>${a.product_name}</td>
                        <td><span style="color:var(--danger)">Critique</span></td>
                        <td>${a.min_stock}</td>
                        <td><span class="badge badge-low">Alerte</span></td>
                    </tr>
                `;
            });
        }
    } catch (err) {
        console.error("Erreur Stats", err);
    }
}

// --- Modales ---
function showModal(id) {
    if (id === 'product-modal' && !document.getElementById('prod-id').value) {
        document.getElementById('product-form').reset();
        document.getElementById('prod-id').value = "";
        document.getElementById('modal-title').innerText = "Ajouter un Produit";
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
