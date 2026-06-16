// AI Logistics - Core App Script (Shared Logic, DB, Algorithms & Simulations) - Phase 4 Updated

// ---------------------------------------------------------
// 1. Initial Mock Database Values & Setup
// ---------------------------------------------------------
const DEPOT = { name: "HQ Depot (Silom)", lat: 13.7251, lng: 100.5302 };

// Products database for order weight calculations
let PRODUCTS = [
    { id: "p1", name: "ปูนซีเมนต์ (Cement Bag)", weight: 50 },  // kg
    { id: "p2", name: "เหล็กเส้น (Steel Rod)", weight: 20 },
    { id: "p3", name: "ถังสีทาบ้าน (Paint Can)", weight: 15 },
    { id: "p4", name: "กระเบื้องมุงหลังคา (Roof Tile)", weight: 8 },
    { id: "p5", name: "กล่องเครื่องมือ (Tool Box)", weight: 12 }
];

function sanitizeProducts(productsArray) {
    if (!Array.isArray(productsArray)) productsArray = [];
    return productsArray.filter(Boolean).map(p => {
        const id = p.id ? String(p.id).trim() : '';
        const name = p.name ? String(p.name).trim() : 'ไม่มีชื่อสินค้า';
        const warehouse = p.warehouse ? String(p.warehouse).trim() : 'สุขสวัสดิ์';
        const unit = p.unit ? String(p.unit).trim() : 'ชิ้น';
        
        let weight = 0;
        if (p.weight !== undefined && p.weight !== null) {
            const parsed = parseFloat(p.weight);
            if (!isNaN(parsed)) weight = parsed;
        }
        
        let qty = 0;
        if (p.qty !== undefined && p.qty !== null) {
            const parsed = parseInt(p.qty);
            if (!isNaN(parsed)) qty = parsed;
        }
        
        const lastUpdated = p.lastUpdated ? String(p.lastUpdated).trim() : '';
        return { id, name, weight, qty, unit, warehouse, lastUpdated };
    });
}

// Bangkok zones mapped with approximate Lat/Lng
const BANGKOK_NODES = {
    HQ: DEPOT,
    Sathorn: { name: "Sathorn (สาทร)", lat: 13.7198, lng: 100.5221 },
    Sukhumvit: { name: "Sukhumvit (สุขุมวิท)", lat: 13.7367, lng: 100.5604 },
    Chatuchak: { name: "Chatuchak (จตุจักร)", lat: 13.8029, lng: 100.5532 },
    BangNa: { name: "Bang Na (บางนา)", lat: 13.6682, lng: 100.6074 },
    Thonburi: { name: "Thonburi (ธนบุรี)", lat: 13.7226, lng: 100.4851 },
    Ladprao: { name: "Ladprao (ลาดพร้าว)", lat: 13.7850, lng: 100.6100 }
};

// Map scale dimensions for coordinate translations
const MAP_LAT_MIN = 13.64;
const MAP_LAT_MAX = 13.83;
const MAP_LNG_MIN = 100.45;
const MAP_LNG_MAX = 100.63;

function latLngToXY(lat, lng, width = 500, height = 300) {
    const x = ((lng - MAP_LNG_MIN) / (MAP_LNG_MAX - MAP_LNG_MIN)) * width;
    const y = (1 - (lat - MAP_LAT_MIN) / (MAP_LAT_MAX - MAP_LAT_MIN)) * height;
    return { x, y };
}

// Helper to get default weight capacity based on driver type (regular vs 3pl) and vehicle type
function getDriverDefaultMaxWeight(driverType, vehicleType) {
    const is3pl = String(driverType).toLowerCase() === '3pl';
    const type = String(vehicleType).toLowerCase();
    
    if (is3pl) {
        if (type.includes("pickup") || type.includes("กระบะ") || type.includes("4ล้อ")) return 3500;
        if (type.includes("truck") || type.includes("บรรทุก") || type.includes("6ล้อ")) return 9000;
        return 3500; // default 3pl
    } else {
        if (type.includes("pickup") || type.includes("กระบะ") || type.includes("4ล้อ")) return 2000;
        if (type.includes("truck") || type.includes("บรรทุก") || type.includes("6ล้อ")) return 5000;
        return 1500; // default regular
    }
}

// Local Database Interface
const DB = {
    get(key, defaultValue = []) {
        const data = localStorage.getItem(`logistics_${key}`);
        let parsed = data ? JSON.parse(data) : defaultValue;
        if (key === 'products') {
            parsed = sanitizeProducts(parsed);
        }
        if (key === 'drivers') {
            let updated = false;
            parsed = parsed.map(d => {
                // Remove motorcycle option in case it was stored
                if (d.vehicleType === 'motorcycle') {
                    d.vehicleType = 'pickup';
                    updated = true;
                }
                
                // Enforce 3PL fixed weights
                if (d.driverType === '3pl') {
                    const fixedW = getDriverDefaultMaxWeight('3pl', d.vehicleType);
                    if (d.maxWeight !== fixedW) {
                        d.maxWeight = fixedW;
                        updated = true;
                    }
                } else {
                    // Backfill regular weights
                    if (d.maxWeight === undefined || d.maxWeight === null) {
                        d.maxWeight = getDriverDefaultMaxWeight(d.driverType || 'regular', d.vehicleType);
                        updated = true;
                    } else {
                        d.maxWeight = parseFloat(d.maxWeight) || getDriverDefaultMaxWeight(d.driverType || 'regular', d.vehicleType);
                    }
                }
                return d;
            });
            if (updated) {
                localStorage.setItem(`logistics_drivers`, JSON.stringify(parsed));
            }
        }
        return parsed;
    },
    set(key, val) {
        if (key === 'products') {
            val = sanitizeProducts(val);
        }
        localStorage.setItem(`logistics_${key}`, JSON.stringify(val));
        if (key === 'products') {
            PRODUCTS = val;
        }
        window.dispatchEvent(new Event('storage-update'));
    },
    resetAll() {
        localStorage.clear();
        this.initDefaultData();
        PRODUCTS = this.get("products");
    },
    initDefaultData() {
        // Init Drivers with regional Warehouses and Plate Provinces
        const defaultDrivers = [
            { id: "drv-1", name: "สมชาย ยอดขนส่ง (Somchai)", phone: "081-234-5678", plate: "1กข-9988", plateProvince: "กรุงเทพฯ", vehicleType: "pickup", warehouse: "สุขสวัสดิ์", status: "approved", driverType: "regular", username: "somchai", password: "somchai123", maxWeight: 2000 },
            { id: "drv-2", name: "วิชัย ใจดี (Wichai)", phone: "089-876-5432", plate: "3กน-4521", plateProvince: "ชลบุรี", vehicleType: "truck", warehouse: "พัทยา", status: "approved", driverType: "regular", username: "wichai", password: "wichai123", maxWeight: 5000 },
            { id: "drv-3", name: "มานะ ขนส่งนอก (Mana)", phone: "085-333-4444", plate: "มข-789", plateProvince: "นครราชสีมา", vehicleType: "pickup", warehouse: "โคราช", status: "pending", driverType: "3pl", maxWeight: 3500 }
        ];
        
        // Init Orders mapped to Suksawat, Pattaya, Korat, Prachinburi
        const defaultOrders = [
            {
                id: "ORD-1024",
                customerName: "ร้าน ABC สาขาบางนา",
                address: BANGKOK_NODES.BangNa.name,
                lat: BANGKOK_NODES.BangNa.lat,
                lng: BANGKOK_NODES.BangNa.lng,
                items: [],
                totalWeight: 0,
                remarks: "ส่งก่อน 10:00 น. ด่วนที่สุด!",
                codAmount: 2450,
                appointmentTime: "09:00 - 11:00",
                priority: "high",
                assignedDriverId: "drv-1",
                routeSequence: 1,
                status: "pending",
                warehouse: "สุขสวัสดิ์",
                createdAt: new Date().toISOString()
            },
            {
                id: "ORD-1025",
                customerName: "ร้านของชำ สาทร (Anan)",
                address: BANGKOK_NODES.Sathorn.name,
                lat: BANGKOK_NODES.Sathorn.lat,
                lng: BANGKOK_NODES.Sathorn.lng,
                items: [],
                totalWeight: 0,
                remarks: "ห้ามส่งตอนเที่ยง",
                codAmount: 1400,
                appointmentTime: "11:00 - 13:00",
                priority: "medium",
                assignedDriverId: "drv-1",
                routeSequence: 2,
                status: "delivering",
                warehouse: "สุขสวัสดิ์",
                createdAt: new Date().toISOString()
            },
            {
                id: "ORD-1026",
                customerName: "ร้านวัสดุจตุจักร (Narin)",
                address: BANGKOK_NODES.Chatuchak.name,
                lat: BANGKOK_NODES.Chatuchak.lat,
                lng: BANGKOK_NODES.Chatuchak.lng,
                items: [],
                totalWeight: 0,
                remarks: "ส่งบ่ายเท่านั้น",
                codAmount: 3200,
                appointmentTime: "13:00 - 15:00",
                priority: "low",
                assignedDriverId: "drv-2",
                routeSequence: 1,
                status: "pending",
                warehouse: "พัทยา",
                createdAt: new Date().toISOString()
            },
            {
                id: "ORD-1027",
                customerName: "บริษัท สุขุมวิท พาร์ทเนอร์ (Pong)",
                address: BANGKOK_NODES.Sukhumvit.name,
                lat: BANGKOK_NODES.Sukhumvit.lat,
                lng: BANGKOK_NODES.Sukhumvit.lng,
                items: [],
                totalWeight: 0,
                remarks: "ส่งก่อน 10:00 น. เท่านั้น",
                codAmount: 16500,
                appointmentTime: "10:00 - 12:00",
                priority: "medium",
                assignedDriverId: "drv-2",
                routeSequence: 2,
                status: "pending",
                warehouse: "พัทยา",
                createdAt: new Date().toISOString()
            },
            {
                id: "ORD-1029",
                customerName: "ฮาร์ดแวร์ฝั่งธนฯ (Tee)",
                address: BANGKOK_NODES.Thonburi.name,
                lat: BANGKOK_NODES.Thonburi.lat,
                lng: BANGKOK_NODES.Thonburi.lng,
                items: [],
                totalWeight: 0,
                remarks: "",
                codAmount: 9600,
                appointmentTime: "15:00 - 17:00",
                priority: "high",
                assignedDriverId: "drv-2",
                routeSequence: 3,
                status: "success",
                paymentStatus: "cash",
                timestamp: new Date().toISOString(),
                warehouse: "พัทยา",
                createdAt: new Date().toISOString()
            },
            {
                id: "ORD-1031",
                customerName: "เคมีภัณฑ์ ลาดพร้าว (Bank)",
                address: BANGKOK_NODES.Ladprao.name,
                lat: BANGKOK_NODES.Ladprao.lat,
                lng: BANGKOK_NODES.Ladprao.lng,
                items: [],
                totalWeight: 0,
                remarks: "ส่งเช้า",
                codAmount: 11200,
                appointmentTime: "13:00 - 15:00",
                priority: "high",
                assignedDriverId: null,
                routeSequence: 0,
                status: "pending",
                warehouse: "โคราช",
                createdAt: new Date().toISOString()
            }
        ];

        const defaultLocations = {
            "drv-1": { driverId: "drv-1", lat: DEPOT.lat, lng: DEPOT.lng, lastActive: new Date().toISOString(), currentStopIndex: 1 },
            "drv-2": { driverId: "drv-2", lat: DEPOT.lat, lng: DEPOT.lng, lastActive: new Date().toISOString(), currentStopIndex: 1 }
        };

        // Populate initial Google Sheet backups matching historical records
        const defaultSheetBackups = [
            {
                timestamp: new Date(Date.now() - 3600000).toISOString(),
                orderId: "ORD-1029",
                customerName: "ฮาร์ดแวร์ฝั่งธนฯ (Tee)",
                warehouse: "พัทยา",
                driverName: "วิชัย ใจดี (Wichai)",
                codAmount: 9600,
                paymentStatus: "cash",
                status: "success",
                podPhoto: "[📷 ดูรูปต้นฉบับ]",
                paymentPhoto: "[📷 ดูสลิปต้นฉบับ]",
                adminNote: "ยอดเงินถูกต้อง ครบถ้วน"
            }
        ];

        // Default Admin HQ Accounts
        const defaultHqAccounts = [
            { id: "hq-1", username: "admin", password: "password123", name: "วิภาดา สมใจ", warehouse: "สุขสวัสดิ์", status: "approved", createdAt: new Date().toISOString() },
            { id: "hq-2", username: "pattaya_admin", password: "pattaya123", name: "เกรียงไกร มีสุข", warehouse: "พัทยา", status: "pending", createdAt: new Date().toISOString() }
        ];

        if (localStorage.getItem("logistics_drivers") === null) {
            localStorage.setItem("logistics_drivers", JSON.stringify(defaultDrivers));
        }
        if (localStorage.getItem("logistics_orders") === null) {
            localStorage.setItem("logistics_orders", JSON.stringify(defaultOrders));
        }
        if (localStorage.getItem("logistics_driverLocations") === null) {
            localStorage.setItem("logistics_driverLocations", JSON.stringify(defaultLocations));
        }
        if (localStorage.getItem("logistics_googleSheetsBackup") === null) {
            localStorage.setItem("logistics_googleSheetsBackup", JSON.stringify(defaultSheetBackups));
        }
        if (localStorage.getItem("logistics_hq_accounts") === null) {
            localStorage.setItem("logistics_hq_accounts", JSON.stringify(defaultHqAccounts));
        }
        const existingProducts = localStorage.getItem("logistics_products");
        if (existingProducts === null || existingProducts === "[]" || JSON.parse(existingProducts).length === 0) {
            const defaultProducts = [
                { id: "p1", name: "ปูนซีเมนต์ (Cement Bag)", weight: 50, qty: 120, warehouse: "สุขสวัสดิ์", lastUpdated: "08:30:00 16/06/2026 (ระบบ)" },
                { id: "p2", name: "เหล็กเส้น (Steel Rod)", weight: 20, qty: 85, warehouse: "สุขสวัสดิ์", lastUpdated: "08:30:00 16/06/2026 (ระบบ)" },
                { id: "p3", name: "ถังสีทาบ้าน (Paint Can)", weight: 15, qty: 200, warehouse: "พัทยา", lastUpdated: "08:30:00 16/06/2026 (ระบบ)" },
                { id: "p4", name: "กระเบื้องมุงหลังคา (Roof Tile)", weight: 8, qty: 450, warehouse: "โคราช", lastUpdated: "08:30:00 16/06/2026 (ระบบ)" },
                { id: "p5", name: "กล่องเครื่องมือ (Tool Box)", weight: 12, qty: 50, warehouse: "ปราจีนบุรี", lastUpdated: "08:30:00 16/06/2026 (ระบบ)" },
                { id: "p6", name: "ท่อ PVC (PVC Pipe)", weight: 2.5, qty: 350, warehouse: "สุขสวัสดิ์", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p7", name: "อิฐบล็อก (Concrete Block)", weight: 1.8, qty: 1200, warehouse: "สุขสวัสดิ์", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p8", name: "แปรงทาสี (Paint Brush)", weight: 0.2, qty: 600, warehouse: "พัทยา", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p9", name: "นั่งร้านเหล็ก (Steel Scaffolding)", weight: 35, qty: 40, warehouse: "พัทยา", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p10", name: "แผ่นเมทัลชีท (Metal Sheet)", weight: 14, qty: 150, warehouse: "พัทยา", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p11", name: "หน้าต่าง UPVC (UPVC Window)", weight: 18, qty: 90, warehouse: "โคราช", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p12", name: "ประตูไม้ (Wooden Door)", weight: 25, qty: 35, warehouse: "โคราช", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p13", name: "สกรูยึดไม้ (Wood Screws Box)", weight: 1.2, qty: 500, warehouse: "โคราช", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p14", name: "ตลับเมตร (Measuring Tape)", weight: 0.3, qty: 450, warehouse: "ปราจีนบุรี", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p15", name: "สว่านไฟฟ้า (Electric Drill)", weight: 3.2, qty: 80, warehouse: "ปราจีนบุรี", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" },
                { id: "p16", name: "เลื่อยวงเดือน (Circular Saw)", weight: 5.5, qty: 25, warehouse: "ปราจีนบุรี", lastUpdated: "08:35:00 16/06/2026 (ระบบ)" }
            ];
            localStorage.setItem("logistics_products", JSON.stringify(defaultProducts));
        }
    }
};

DB.initDefaultData();
PRODUCTS = DB.get("products", PRODUCTS);

// ---------------------------------------------------------
// 2. Heuristic Functions
// ---------------------------------------------------------
function calculateDistance(lat1, lng1, lat2, lng2) {
    if (!lat1 || !lng1 || !lat2 || !lng2) return 0;
    const dLat = lat2 - lat1;
    const dLng = lng2 - lng1;
    return Math.sqrt(dLat * dLat + dLng * dLng) * 111;
}

function getConstraintTime(ord) {
    if (!ord.remarks) return 99;
    const text = ord.remarks.toLowerCase();
    
    // Explicit keywords
    if (text.includes("ด่วนที่สุด") || text.includes("ด่วนมาก") || text.includes("ด่วนที่สุด!")) return 6.0;
    if (text.includes("ด่วน")) return 7.0;
    if (text.includes("ส่งเช้า")) return 8.5;
    if (text.includes("ก่อนเที่ยง")) return 12.0;

    // Detect patterns like "ก่อน 8.00 น.", "ก่อน 8:00", "ก่อน 8"
    const timeMatch = text.match(/ก่อน\s*(\d+)(?:[:\.](\d+))?/);
    if (timeMatch) {
        const hr = parseInt(timeMatch[1]);
        const min = timeMatch[2] ? parseInt(timeMatch[2]) : 0;
        return hr + (min / 60);
    }
    
    // Explicit times like "8:00", "8.00"
    const explicitMatch = text.match(/\b(\d{1,2})[:\.](\d{2})\b/);
    if (explicitMatch) {
        const hr = parseInt(explicitMatch[1]);
        const min = parseInt(explicitMatch[2]);
        if (hr <= 15) { // morning/afternoon constraints
            return hr + (min / 60);
        }
    }
    
    return 99;
}

function hasTimeConstraint(ord) {
    return getConstraintTime(ord) < 99;
}

function optimizeRoutes(orderStops, mode = 'fastest') {
    if (orderStops.length <= 1) return orderStops;
    
    // Time constraint jobs must be completed first
    let constrained = orderStops.filter(o => getConstraintTime(o) < 99);
    let normal = orderStops.filter(o => getConstraintTime(o) >= 99);
    
    let route = [];
    let currentLat = DEPOT.lat;
    let currentLng = DEPOT.lng;

    // 1. Process Constrained stops first (Earliest Deadline First with Nearest Neighbor)
    let unvisitedConstrained = [...constrained];
    while (unvisitedConstrained.length > 0) {
        let minDeadline = Math.min(...unvisitedConstrained.map(getConstraintTime));
        let candidates = unvisitedConstrained.filter(o => getConstraintTime(o) <= minDeadline + 0.25);
        
        let nearestIdx = -1;
        let minDistance = Infinity;
        
        for (let i = 0; i < candidates.length; i++) {
            let d = calculateDistance(currentLat, currentLng, candidates[i].lat, candidates[i].lng);
            if (d < minDistance) {
                minDistance = d;
                nearestIdx = unvisitedConstrained.indexOf(candidates[i]);
            }
        }
        
        let nextStop = unvisitedConstrained.splice(nearestIdx, 1)[0];
        route.push(nextStop);
        currentLat = nextStop.lat;
        currentLng = nextStop.lng;
    }

    // 2. Process Normal stops (Nearest Neighbor according to mode)
    let unvisitedNormal = [...normal];
    if (mode === 'fastest') {
        while (unvisitedNormal.length > 0) {
            let nearestIdx = -1;
            let minDistance = Infinity;
            
            for (let i = 0; i < unvisitedNormal.length; i++) {
                let d = calculateDistance(currentLat, currentLng, unvisitedNormal[i].lat, unvisitedNormal[i].lng);
                if (d < minDistance) {
                    minDistance = d;
                    nearestIdx = i;
                }
            }
            
            let nextStop = unvisitedNormal.splice(nearestIdx, 1)[0];
            route.push(nextStop);
            currentLat = nextStop.lat;
            currentLng = nextStop.lng;
        }
    } 
    else if (mode === 'eco') {
        while (unvisitedNormal.length > 0) {
            let bestIdx = -1;
            let lowestCost = Infinity;

            for (let i = 0; i < unvisitedNormal.length; i++) {
                const item = unvisitedNormal[i];
                const dist = calculateDistance(currentLat, currentLng, item.lat, item.lng);
                const ecoCost = dist;

                if (ecoCost < lowestCost) {
                    lowestCost = ecoCost;
                    bestIdx = i;
                }
            }

            let nextStop = unvisitedNormal.splice(bestIdx, 1)[0];
            route.push(nextStop);
            currentLat = nextStop.lat;
            currentLng = nextStop.lng;
        }
    } 
    else if (mode === 'priority') {
        const priorityWeight = { high: 3, medium: 2, low: 1 };
        
        while (unvisitedNormal.length > 0) {
            let bestIdx = -1;
            let highestPriorityScore = -Infinity;

            for (let i = 0; i < unvisitedNormal.length; i++) {
                const item = unvisitedNormal[i];
                const dist = calculateDistance(currentLat, currentLng, item.lat, item.lng);
                
                let startHour = 12;
                if (item.appointmentTime) {
                    const match = item.appointmentTime.match(/^(\d+):/);
                    if (match) startHour = parseInt(match[1]);
                }

                const pScore = (priorityWeight[item.priority] * 10) - (startHour * 1.5) - (dist * 0.2);

                if (pScore > highestPriorityScore) {
                    highestPriorityScore = pScore;
                    bestIdx = i;
                }
            }

            let nextStop = unvisitedNormal.splice(bestIdx, 1)[0];
            route.push(nextStop);
            currentLat = nextStop.lat;
            currentLng = nextStop.lng;
        }
    }

    return route.map((ord, idx) => {
        ord.routeSequence = idx + 1;
        return ord;
    });
}

// ---------------------------------------------------------
// 3. Mock Assets
// ---------------------------------------------------------
function createMockImageBase64(text, bgGradientColors = ["#3b82f6", "#8b5cf6"]) {
    const canvas = document.createElement("canvas");
    canvas.width = 400;
    canvas.height = 300;
    const ctx = canvas.getContext("2d");

    const grad = ctx.createLinearGradient(0, 0, 400, 300);
    grad.addColorStop(0, bgGradientColors[0]);
    grad.addColorStop(1, bgGradientColors[1]);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 400, 300);

    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.lineWidth = 2;
    for (let i = 0; i < 400; i += 40) {
        ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i + 100, 300); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(400, i + 100); ctx.stroke();
    }

    ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
    ctx.lineWidth = 15;
    ctx.strokeRect(10, 10, 380, 280);

    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(200, 100, 35, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = bgGradientColors[0];
    ctx.font = "24px 'Outfit'";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("📷", 200, 100);

    ctx.fillStyle = "white";
    ctx.font = "bold 16px 'Sarabun'";
    ctx.fillText(text, 200, 175);

    ctx.font = "12px 'Sarabun'";
    ctx.fillStyle = "rgba(255,255,255,0.7)";
    ctx.fillText("หลักฐานการนำส่งสินค้า (POD)", 200, 210);
    ctx.fillText("เวลาบันทึก: " + new Date().toLocaleTimeString(), 200, 230);
    ctx.fillText("พิกัดนำส่ง: 13.726 / 100.532", 200, 250);

    return canvas.toDataURL("image/jpeg");
}

// ---------------------------------------------------------
// 4. GPS Simulated Path Movement Engine
// ---------------------------------------------------------
let simulationIntervals = {};

function startGPSSimulator(driverId, onStepCallback) {
    if (simulationIntervals[driverId]) {
        clearInterval(simulationIntervals[driverId]);
    }

    const orders = DB.get("orders");
    const locations = DB.get("driverLocations");
    const currentLoc = locations[driverId] || { lat: DEPOT.lat, lng: DEPOT.lng, driverId: driverId, currentStopIndex: 1 };
    
    const activeRoute = orders
        .filter(o => o.assignedDriverId === driverId && (o.status === "pending" || o.status === "delivering" || o.status === "request_info" || o.status === "rejected_pod"))
        .sort((a, b) => a.routeSequence - b.routeSequence);
    
    if (activeRoute.length === 0) {
        if (onStepCallback) onStepCallback(null, "No pending delivery jobs assigned.");
        return;
    }

    const currentJob = activeRoute[0];
    if (currentJob.status !== "delivering") {
        currentJob.status = "delivering";
        DB.set("orders", orders);
    }

    const startLat = currentLoc.lat;
    const startLng = currentLoc.lng;
    const destLat = currentJob.lat;
    const destLng = currentJob.lng;
    
    let step = 0;
    const totalSteps = 15;
    
    simulationIntervals[driverId] = setInterval(() => {
        step++;
        const ratio = step / totalSteps;
        
        const currentLatStep = startLat + (destLat - startLat) * ratio;
        const currentLngStep = startLng + (destLng - startLng) * ratio;
        
        const updatedLocations = DB.get("driverLocations");
        updatedLocations[driverId] = {
            driverId: driverId,
            lat: currentLatStep,
            lng: currentLngStep,
            lastActive: new Date().toISOString(),
            currentStopIndex: currentJob.routeSequence
        };
        DB.set("driverLocations", updatedLocations);
        
        if (onStepCallback) {
            onStepCallback({
                lat: currentLatStep,
                lng: currentLngStep,
                progress: ratio,
                activeJob: currentJob
            });
        }
        
        if (step >= totalSteps) {
            clearInterval(simulationIntervals[driverId]);
            delete simulationIntervals[driverId];
            
            if (onStepCallback) {
                onStepCallback({
                    lat: destLat,
                    lng: destLng,
                    progress: 1.0,
                    activeJob: currentJob,
                    arrived: true
                });
            }
        }
    }, 400);
}

function stopGPSSimulator(driverId) {
    if (simulationIntervals[driverId]) {
        clearInterval(simulationIntervals[driverId]);
        delete simulationIntervals[driverId];
    }
}

// ---------------------------------------------------------
// 5. Excel & CSV Item-Line Parser
// ---------------------------------------------------------
function parseExcelItemLine(itemLine) {
    if (!itemLine) return [{ name: "สินค้าเหมาน้ำหนัก (Bulk Items)", weight: 10, qty: 1 }];
    
    const items = [];
    const parts = itemLine.split(/[,;]/);
    
    parts.forEach(part => {
        const trimmed = part.trim();
        if (!trimmed) return;
        
        const match = trimmed.match(/^(.+?)\s*[xX**]\s*(\d+)$/) || trimmed.match(/^(\d+)\s*(.+?)$/);
        let name = trimmed;
        let qty = 1;
        
        if (match) {
            if (isNaN(match[1])) {
                name = match[1].trim();
                qty = parseInt(match[2]);
            } else {
                qty = parseInt(match[1]);
                name = match[2].trim();
            }
        }
        
        let unitWeight = 10;
        const standardProd = PRODUCTS.find(p => p.name.toLowerCase().includes(name.toLowerCase()) || name.toLowerCase().includes(p.name.split(' ')[0].toLowerCase()));
        
        if (standardProd) {
            unitWeight = standardProd.weight;
        } else {
            const weightHint = name.match(/(\d+)\s*(?:kg|กิโล|กิโลกรัม)/i);
            if (weightHint) {
                unitWeight = parseFloat(weightHint[1]);
            }
        }
        
        items.push({
            name: name,
            weight: unitWeight,
            qty: qty
        });
    });
    
    return items;
}

function parseCSVText(text) {
    const lines = text.split('\n');
    if (lines.length < 2) return [];

    // Strip BOM if present
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, '').replace(/^\ufeff/, ''));
    const orders = [];

    // Helper: find value by header name (multiple aliases) or fallback column index
    const getColumnVal = (rowValues, keyArray, fallbackIndex) => {
        for (const key of keyArray) {
            const idx = headers.findIndex(h =>
                h.toLowerCase().trim() === key.toLowerCase().trim() ||
                h.trim() === key.trim()
            );
            if (idx !== -1 && rowValues[idx] !== undefined && rowValues[idx] !== '') {
                return rowValues[idx].trim().replace(/"/g, '');
            }
        }
        if (fallbackIndex !== undefined && fallbackIndex < rowValues.length && rowValues[fallbackIndex] !== undefined) {
            return rowValues[fallbackIndex].trim().replace(/"/g, '');
        }
        return null;
    };

    for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;

        // Robust CSV split: handle commas inside quoted fields
        let rowValues = [];
        let inQuotes = false;
        let currentVal = '';
        for (let charIdx = 0; charIdx < line.length; charIdx++) {
            const c = line[charIdx];
            if (c === '"') {
                inQuotes = !inQuotes;
            } else if (c === ',' && !inQuotes) {
                rowValues.push(currentVal);
                currentVal = '';
            } else {
                currentVal += c;
            }
        }
        rowValues.push(currentVal);
        rowValues = rowValues.map(v => v.trim());

        // ─── Column mapping (ตามรูปแบบใหม่) ───────────────────────────────────
        // Col 0: IV-ID / stop_id
        // Col 1: latitude / lat
        // Col 2: longitude / lng
        // Col 3: หมายเลขลูกค้า / customer_id
        // Col 4: service_time (นาที)
        // Col 5: น้ำหนักของสินค้า / weight
        // Col 6: dropoffs  (1 = ส่งของ default, 0 = ไปรับของ/รับกลับ)
        // Col 7: ชื่อร้านค้า / name
        // Col 8: บันทึก / note
        // ────────────────────────────────────────────────────────────────────

        const id = getColumnVal(rowValues,
            ["IV-ID", "stop_id", "Stop ID", "id", "หมายเลขจุดส่ง"],
            0) || `ORD-${1000 + Math.floor(Math.random() * 9000)}`;

        const latVal  = getColumnVal(rowValues, ["lat", "latitude", "ละติจูด",  "Latitude"],  1);
        const lngVal  = getColumnVal(rowValues, ["lng", "longitude", "ลองจิจูด", "Longitude"], 2);

        const customerId = getColumnVal(rowValues,
            ["customer_id", "หมายเลขลูกค้า", "customerName", "Customer", "ชื่อลูกค้า"],
            3) || '';

        const serviceTimeVal = getColumnVal(rowValues,
            ["service_time", "serviceTime", "เวลาบริการ", "ระยะเวลาให้บริการ"],
            4);

        const weightVal = getColumnVal(rowValues,
            ["weight", "น้ำหนักของสินค้า", "น้ำหนัก", "Weight"],
            5);

        const dropoffsVal = getColumnVal(rowValues,
            ["dropoffs", "ไม่ส่งของ ใส่ 1", "ส่ง/รับ"],
            6);

        // ชื่อร้านค้า (ใช้เป็นชื่อหลักแสดงในระบบ)
        const shopName = getColumnVal(rowValues,
            ["name", "ชื่อร้านค้า", "ชื่อร้าน", "shopName"],
            7);

        const note = getColumnVal(rowValues,
            ["note", "บันทึก", "หมายเหตุ", "Remarks", "remarks"],
            8) || '';

        // ─── Skip header-like rows ────────────────────────────────────────
        if (id && (id.toLowerCase().includes('stop_id') || id.toLowerCase() === 'iv-id' || id.toLowerCase() === 'id')) continue;
        if (customerId && (customerId.toLowerCase().includes('customer') || customerId.includes('หมายเลขลูกค้า'))) continue;

        const lat = parseFloat(latVal);
        const lng = parseFloat(lngVal);
        if (isNaN(lat) || isNaN(lng)) continue; // ต้องมีพิกัด

        const weight      = parseFloat((weightVal  || '0').replace(/,/g, '')) || 0;
        const serviceTime = parseInt(serviceTimeVal) || 0;

        // ชื่อที่แสดงในระบบ: ใช้ shopName ก่อน ถ้าไม่มีใช้ customerId
        const displayName = (shopName && shopName.trim()) || (customerId && customerId.trim()) || `จุดส่ง (${lat.toFixed(4)}, ${lng.toFixed(4)})`;

        // dropoffs: 1 = delivery (default), 0 = return/pickup
        const dropoffNum = dropoffsVal !== null ? parseInt(dropoffsVal) : 1;
        let orderType = 'delivery';
        if (dropoffNum === 0) {
            orderType = 'return';
        } else if (note && (note.includes('รับกลับ') || note.includes('คืนสินค้า') || note.includes('รับคืน') || note.includes('เก็บคืน') || note.includes('เก็บสินค้า'))) {
            orderType = 'return';
        }

        orders.push({
            id:               id,
            type:             orderType,
            customerName:     displayName,
            customerId:       customerId,
            address:          note ? `${displayName} (${note})` : displayName,
            lat,
            lng,
            serviceTime,
            items:            [{ name: displayName, weight: weight, qty: 1 }],
            totalWeight:      weight,
            remarks:          note,
            codAmount:        0,
            appointmentTime:  '09:00 - 17:00',
            priority:         'medium',
            assignedDriverId: null,
            routeSequence:    0,
            status:           'pending',
            warehouse:        'สุขสวัสดิ์',
            createdAt:        new Date().toISOString()
        });
    }
    return orders;
}

// ---------------------------------------------------------
// 6. Google Sheets Simulated Backup Logger (Phase 4 Additions)
// ---------------------------------------------------------
function backupOrderToGoogleSheet(order) {
    const backupLogs = DB.get("googleSheetsBackup", []);
    const drivers = DB.get("drivers");
    
    const driverObj = drivers.find(d => d.id === order.assignedDriverId);
    const driverLabel = driverObj ? `${driverObj.name} (${driverObj.plate} ${driverObj.plateProvince})` : 'ไม่ได้มอบหมาย';
    
    // Check if row already exist to update it, otherwise push new row
    const rowIdx = backupLogs.findIndex(row => row.orderId === order.id);
    
    const rowData = {
        timestamp: new Date().toISOString(),
        orderId: order.id,
        customerName: order.customerName,
        warehouse: order.warehouse,
        driverName: driverLabel,
        codAmount: order.codAmount,
        paymentStatus: order.paymentStatus || 'unpaid',
        status: order.status,
        podPhoto: order.podPhoto ? "[📷 ดูรูปต้นฉบับ]" : "ไม่มีรูปภาพแนบ",
        paymentPhoto: order.paymentPhoto ? "[📷 ดูสลิปต้นฉบับ]" : "ไม่มีรูปหลักฐาน",
        adminNote: order.adminNote || ""
    };

    if (rowIdx !== -1) {
        backupLogs[rowIdx] = rowData;
    } else {
        backupLogs.push(rowData);
    }

    DB.set("googleSheetsBackup", backupLogs);
}

function deductStockFromOrder(order) {
    if (!order || !order.items || order.items.length === 0) return;
    const products = DB.get("products");
    let updated = false;

    order.items.forEach(item => {
        const idx = products.findIndex(p => 
            p.id.toLowerCase() === item.name.toLowerCase() ||
            p.name.toLowerCase().trim() === item.name.toLowerCase().trim() ||
            p.name.toLowerCase().includes(item.name.toLowerCase()) ||
            item.name.toLowerCase().includes(p.name.split(' ')[0].toLowerCase())
        );

        if (idx !== -1) {
            const qtyToDeduct = parseInt(item.qty) || 0;
            products[idx].qty = Math.max(0, (products[idx].qty || 0) - qtyToDeduct);
            updated = true;
        }
    });

    if (updated) {
        DB.set("products", products);
    }
}

// ---------------------------------------------------------
// 7. Admin HQ Audit Actions
// ---------------------------------------------------------
function auditApproveAndClose(orderId, adminNote) {
    const orders = DB.get("orders");
    const idx = orders.findIndex(o => o.id === orderId);
    if (idx !== -1) {
        orders[idx].status = 'success';
        orders[idx].adminNote = adminNote || "อนุมัติผ่านการตรวจสอบ";
        orders[idx].reviewedAt = new Date().toISOString();
        
        // Deduct quantities from stock
        deductStockFromOrder(orders[idx]);
        
        DB.set("orders", orders);
        
        // Backup to Google Sheet simulation
        backupOrderToGoogleSheet(orders[idx]);
        
        return true;
    }
    return false;
}

function auditRejectPOD(orderId, adminNote) {
    const orders = DB.get("orders");
    const idx = orders.findIndex(o => o.id === orderId);
    if (idx !== -1) {
        orders[idx].status = 'rejected_pod';
        orders[idx].adminNote = adminNote || "หลักฐานไม่ชัดเจน โปรดถ่ายแก้ไขอัปโหลดส่งใหม่";
        orders[idx].reviewedAt = new Date().toISOString();
        
        DB.set("orders", orders);
        
        backupOrderToGoogleSheet(orders[idx]);
        
        return true;
    }
    return false;
}

function auditRequestMoreInfo(orderId, adminNote) {
    const orders = DB.get("orders");
    const idx = orders.findIndex(o => o.id === orderId);
    if (idx !== -1) {
        orders[idx].status = 'request_info';
        orders[idx].adminNote = adminNote || "ต้องการเอกสารแนบยืนยันเพิ่มเติม";
        orders[idx].reviewedAt = new Date().toISOString();
        
        DB.set("orders", orders);
        
        backupOrderToGoogleSheet(orders[idx]);
        
        return true;
    }
    return false;
}

// Hamburger Mobile Navigation Logic
function toggleMobileMenu() {
    const sidebar = document.querySelector('.hq-sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar) sidebar.classList.toggle('active');
    if (overlay) overlay.classList.toggle('active');
}
