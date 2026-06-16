import os
import re

def modify_admin_html():
    print("Modifying admin.html...")
    with open("admin.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. HTML tab-drivers replacement
    original_tab_drivers = """            <div id="tab-drivers" class="tab-content">
                <div class="hq-panel">
                    <div class="hq-panel-header">
                        <h3 class="hq-panel-title">ทำเนียบพนักงานจัดส่ง & จัดการอนุมัติสิทธิ์ (3PL)</h3>
                    </div>
                    <div class="hq-table-container">
                        <table class="hq-table">
                            <thead>
                                <tr>
                                    <th>รหัสระบบ</th>
                                    <th>ประเภท</th>
                                    <th>ชื่อ-นามสกุล</th>
                                    <th>เบอร์โทรศัพท์</th>
                                    <th>เลขทะเบียน</th>
                                    <th>จังหวัดทะเบียน</th>
                                    <th>คลังสินค้าที่รับงาน</th>
                                    <th>ประเภทพาหนะ</th>
                                    <th>การอนุมัติสิทธิ์</th>
                                    <th>คำสั่ง</th>
                                </tr>
                            </thead>
                            <tbody id="driverTableBody">
                                <!-- Injected by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>"""

    new_tab_drivers = """            <div id="tab-drivers" class="tab-content">
                <!-- DRIVERS EXCEL UPLOAD PANEL -->
                <div class="hq-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
                    <div class="hq-panel-header" style="margin-bottom: 1.25rem; border-bottom: 1px solid var(--hq-border); padding-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                        <h3 class="hq-panel-title">📥 นำเข้าข้อมูลคนขับ & อัปเดตทะเบียน/น้ำหนักบรรทุก (Excel)</h3>
                        
                        <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
                            <!-- Sample Template Download Button -->
                            <button onclick="downloadSampleDriverCSV()" class="btn btn-outline" style="padding: 0.45rem 0.9rem; font-size: 0.8rem; font-weight: bold; border-color: #10b981; color: #10b981; display: flex; align-items: center; gap: 6px; background: rgba(16, 185, 129, 0.02);">
                                📋 ดาวน์โหลดไฟล์ตัวอย่าง CSV คนขับ
                            </button>
                            
                            <!-- Excel Upload button -->
                            <button onclick="document.getElementById('driverExcelFileInput').click()" class="btn btn-primary" style="padding: 0.45rem 1rem; font-size: 0.8rem; font-weight: 700; background: linear-gradient(135deg, #0284c7, #0369a1); border: none; display: flex; align-items: center; gap: 6px;">
                                📥 อัปโหลด Excel
                            </button>
                            <input type="file" id="driverExcelFileInput" style="display: none;" accept=".xlsx, .xls, .csv" onchange="handleDriverExcelUpload(this)">
                        </div>
                    </div>

                    <!-- Drag-and-drop Excel upload zone for Drivers -->
                    <div id="driverExcelDropZone" class="excel-upload-zone" style="cursor: pointer; padding: 1.5rem; border: 2px dashed rgba(59, 130, 246, 0.3); background: rgba(59, 130, 246, 0.02); border-radius: 16px; text-align: center; transition: all 0.3s;"
                         onclick="document.getElementById('driverExcelFileInput').click()"
                         ondragover="event.preventDefault(); this.style.borderColor='var(--color-primary)';"
                         ondragleave="this.style.borderColor='';"
                         ondrop="handleDriverExcelDrop(event)">
                        <span style="font-size: 1.8rem;">🚚</span>
                        <strong style="color: white; font-size: 0.9rem; display: block; margin-top: 0.3rem;">ลากไฟล์ Excel / CSV อัปเดตน้ำหนักคนขับมาวางที่นี่ หรือคลิกเพื่ออัปโหลด</strong>
                        <span style="font-size: 0.72rem; color: var(--hq-text-muted);">รองรับคอลัมน์: รหัสระบบ (ถ้ามี), เลขทะเบียน, จังหวัดทะเบียน, ชื่อพนักงาน, ประเภทคนขับ, ประเภทพาหนะ, น้ำหนักบรรทุกสูงสุด (กก.), คลังสินค้า</span>
                    </div>
                </div>

                <div class="hq-panel">
                    <div class="hq-panel-header">
                        <h3 class="hq-panel-title">ทำเนียบพนักงานจัดส่ง & จัดการอนุมัติสิทธิ์ (3PL)</h3>
                    </div>
                    <div class="hq-table-container">
                        <table class="hq-table">
                            <thead>
                                <tr>
                                    <th>รหัสระบบ</th>
                                    <th>ประเภท</th>
                                    <th>ชื่อ-นามสกุล</th>
                                    <th>เบอร์โทรศัพท์</th>
                                    <th>เลขทะเบียน</th>
                                    <th>จังหวัดทะเบียน</th>
                                    <th>คลังสินค้าที่รับงาน</th>
                                    <th>ประเภทพาหนะ</th>
                                    <th>น้ำหนักบรรทุกสูงสุด (Max Capacity)</th>
                                    <th>การอนุมัติสิทธิ์</th>
                                    <th>คำสั่ง</th>
                                </tr>
                            </thead>
                            <tbody id="driverTableBody">
                                <!-- Injected by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>"""

    if original_tab_drivers in content:
        content = content.replace(original_tab_drivers, new_tab_drivers)
        print("  - tab-drivers HTML updated.")
    else:
        # Fallback split search
        print("  - WARNING: exact original_tab_drivers not matched, doing regex search...")
        content = re.sub(r'<div id="tab-drivers" class="tab-content">[\s\S]*?</table>\s*</div>\s*</div>\s*</div>', new_tab_drivers, content)

    # 2. HTML driverRouteReportModal baton pass section
    original_modal_list = """            <!-- Route Stop List -->
            <div style="background: rgba(255, 255, 255, 0.01); border: 1px solid var(--hq-border); border-radius: 20px; padding: 1.25rem; max-height: 400px; overflow-y: auto;">
                <div id="reportRouteStopList" style="display: flex; flex-direction: column; gap: 1rem;">
                    <!-- Injected by JS -->
                </div>
            </div>"""

    new_modal_list = """            <!-- Route Stop List -->
            <div style="background: rgba(255, 255, 255, 0.01); border: 1px solid var(--hq-border); border-radius: 20px; padding: 1.25rem; max-height: 220px; overflow-y: auto;">
                <div id="reportRouteStopList" style="display: flex; flex-direction: column; gap: 1rem;">
                    <!-- Injected by JS -->
                </div>
            </div>

            <!-- Route Baton Pass / Reassignment Section -->
            <div id="routeTransferSection" style="background: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 16px; padding: 1rem; margin-top: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                <h4 style="font-size: 0.85rem; color: white; font-weight: bold; margin: 0; display: flex; align-items: center; gap: 6px;">
                    🔄 โอนเส้นทางจัดส่งทั้งหมด (Baton Pass / Reassignment)
                </h4>
                <p style="font-size: 0.7rem; color: var(--hq-text-muted); margin: 0; line-height: 1.45;">
                    คุณสามารถโอนคิวงานทั้งหมดของรถคันนี้ ให้กับคนขับรถประจำหรือรถขนส่งนอกอื่นได้
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <div>
                        <label style="font-size: 0.65rem; color: var(--hq-text-muted); display: block; margin-bottom: 2px;">โอนงานประเภท</label>
                        <select id="transferTypeSelect" class="form-select" style="width: 100%; padding: 0.45rem; font-size: 0.8rem; background: #0f172a; border-radius: 8px; border: 1px solid var(--hq-border); color: white;">
                            <option value="all_pending">งานค้างทั้งหมด (All Pending)</option>
                            <option value="returns_only">เฉพาะงานรับสินค้ากลับ (Returns Only)</option>
                        </select>
                    </div>
                    <div>
                        <label style="font-size: 0.65rem; color: var(--hq-text-muted); display: block; margin-bottom: 2px;">โอนไปให้คนขับ</label>
                        <select id="transferTargetDriverSelect" class="form-select" style="width: 100%; padding: 0.45rem; font-size: 0.8rem; background: #0f172a; border-radius: 8px; border: 1px solid var(--hq-border); color: white;">
                            <!-- Injected dynamically by JS -->
                        </select>
                    </div>
                </div>
                <button id="btnConfirmRouteTransfer" class="btn btn-primary btn-sm" style="padding: 0.5rem; font-size: 0.8rem; font-weight: 700; background: linear-gradient(135deg, var(--color-primary), var(--color-secondary)); border: none; border-radius: 8px; width: 100%; cursor: pointer;" onclick="executeRouteTransferFromModal()">
                    ✅ ยืนยันโอนเส้นทาง
                </button>
            </div>"""

    if original_modal_list in content:
        content = content.replace(original_modal_list, new_modal_list)
        print("  - driverRouteReportModal HTML updated.")
    else:
        print("  - ERROR: original_modal_list not found!")

    # 3. HTML driverQueuePreviewPanel header buttons
    original_queue_header = """                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="width:28px; height:28px; border-radius:50%; background: rgba(245,158,11,0.2); border: 1px solid var(--color-warning); display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:800; color:var(--color-warning); flex-shrink:0;">3</div>
                                    <h3 style="font-size: 1rem; font-weight: 700; color: white; margin: 0;" id="driverQueueTitle">คิวงานคนขับที่เลือก</h3>
                                </div>
                                <button class="btn btn-outline btn-sm" style="font-size: 0.75rem;" onclick="triggerOptimizationForSelected()">🔄 จัดลำดับใหม่</button>
                            </div>"""

    new_queue_header = """                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="width:28px; height:28px; border-radius:50%; background: rgba(245,158,11,0.2); border: 1px solid var(--color-warning); display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:800; color:var(--color-warning); flex-shrink:0;">3</div>
                                    <h3 style="font-size: 1rem; font-weight: 700; color: white; margin: 0;" id="driverQueueTitle">คิวงานคนขับที่เลือก</h3>
                                </div>
                                <div style="display: flex; gap: 6px;">
                                    <button class="btn btn-outline btn-sm" style="font-size: 0.75rem; border-color: var(--color-secondary); color: var(--color-secondary);" onclick="openQueueTransferQuick()">🔄 โอนย้ายคิว</button>
                                    <button class="btn btn-outline btn-sm" style="font-size: 0.75rem;" onclick="triggerOptimizationForSelected()">⚡ จัดคิวใหม่</button>
                                </div>
                            </div>"""

    if original_queue_header in content:
        content = content.replace(original_queue_header, new_queue_header)
        print("  - driverQueuePreviewPanel header HTML updated.")
    else:
        print("  - ERROR: original_queue_header not found!")

    # 4. JS renderDriversTable replacement
    original_render_drivers_table = """        function renderDriversTable() {
            let drivers = DB.get("drivers");
            if (hqSessionWarehouse !== 'all') {
                drivers = drivers.filter(d => d.warehouse === hqSessionWarehouse);
            }
            const tbody = document.getElementById('driverTableBody');
            tbody.innerHTML = '';

            if (drivers.length === 0) {
                tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; color:var(--hq-text-muted); padding:2rem;">ไม่มีรายชื่อพนักงานจัดส่งในระบบ</td></tr>`;
                return;
            }

            drivers.forEach(drv => {
                let statusBadge = '';
                let actionBtn = '';

                if (drv.status === 'pending') {
                    statusBadge = `<span class="badge badge-pending">รออนุมัติ</span>`;
                    actionBtn = `
                        <button class="btn btn-primary btn-sm" onclick="updateDriverStatus('${drv.id}', 'approved')" style="background:var(--color-success);">อนุมัติ</button>
                        <button class="btn btn-outline btn-sm" onclick="updateDriverStatus('${drv.id}', 'rejected')" style="color:var(--color-danger); border-color:rgba(239,68,68,0.2);">ปฏิเสธ</button>
                    `;
                } else if (drv.status === 'approved') {
                    statusBadge = `<span class="badge badge-approved">อนุมัติแล้ว</span>`;
                    actionBtn = `<button class="btn btn-outline btn-sm" onclick="updateDriverStatus('${drv.id}', 'pending')">ระงับชั่วคราว</button>`;
                } else {
                    statusBadge = `<span class="badge badge-rejected">ปฏิเสธสิทธิ์</span>`;
                    actionBtn = `<button class="btn btn-primary btn-sm" onclick="updateDriverStatus('${drv.id}', 'approved')" style="background:var(--color-success);">อนุมัติอีกครั้ง</button>`;
                }

                const vehicleMapping = {
                    pickup: "กระบะ 4 ล้อ (Pickup)",
                    truck: "บรรทุก 6 ล้อใหญ่ (Truck)",
                    motorcycle: "จักรยานยนต์ (Motorcycle)"
                };

                const typeLabel = drv.driverType === 'regular' ? 
                    `<span style="background:rgba(37, 99, 235, 0.1); color:var(--color-primary); padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">คนขับประจำ</span>` : 
                    `<span style="background:rgba(139, 92, 246, 0.1); color:var(--color-secondary); padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">ขนส่งนอก</span>`;

                tbody.innerHTML += `
                    <tr>
                        <td style="font-family:var(--font-heading); font-weight:600;">${drv.id}</td>
                        <td>${typeLabel}</td>
                        <td><strong>${drv.name}</strong></td>
                        <td>${drv.phone}</td>
                        <td>${drv.plate}</td>
                        <td><strong>${drv.plateProvince || 'ไม่ระบุ'}</strong></td>
                        <td><span style="color: var(--color-secondary); font-weight: 600;">${drv.warehouse || 'สุขสวัสดิ์'}</span></td>
                        <td>${vehicleMapping[drv.vehicleType] || drv.vehicleType}</td>
                        <td>${statusBadge}</td>
                        <td><div style="display:flex; gap:0.5rem;">${actionBtn}</div></td>
                    </tr>
                `;
            });
        }"""

    new_render_drivers_table = """        function renderDriversTable() {
            let drivers = DB.get("drivers");
            if (hqSessionWarehouse !== 'all') {
                drivers = drivers.filter(d => d.warehouse === hqSessionWarehouse);
            }
            const tbody = document.getElementById('driverTableBody');
            tbody.innerHTML = '';

            if (drivers.length === 0) {
                tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; color:var(--hq-text-muted); padding:2rem;">ไม่มีรายชื่อพนักงานจัดส่งในระบบ</td></tr>`;
                return;
            }

            drivers.forEach(drv => {
                let statusBadge = '';
                let actionBtn = '';

                if (drv.status === 'pending') {
                    statusBadge = `<span class="badge badge-pending">รออนุมัติ</span>`;
                    actionBtn = `
                        <button class="btn btn-primary btn-sm" onclick="updateDriverStatus('${drv.id}', 'approved')" style="background:var(--color-success);">อนุมัติ</button>
                        <button class="btn btn-outline btn-sm" onclick="updateDriverStatus('${drv.id}', 'rejected')" style="color:var(--color-danger); border-color:rgba(239,68,68,0.2);">ปฏิเสธ</button>
                    `;
                } else if (drv.status === 'approved') {
                    statusBadge = `<span class="badge badge-approved">อนุมัติแล้ว</span>`;
                    actionBtn = `<button class="btn btn-outline btn-sm" onclick="updateDriverStatus('${drv.id}', 'pending')">ระงับชั่วคราว</button>`;
                } else {
                    statusBadge = `<span class="badge badge-rejected">ปฏิเสธสิทธิ์</span>`;
                    actionBtn = `<button class="btn btn-primary btn-sm" onclick="updateDriverStatus('${drv.id}', 'approved')" style="background:var(--color-success);">อนุมัติอีกครั้ง</button>`;
                }

                const vehicleMapping = {
                    pickup: "กระบะ 4 ล้อ (Pickup)",
                    truck: "บรรทุก 6 ล้อใหญ่ (Truck)"
                };

                const typeLabel = drv.driverType === 'regular' ? 
                    `<span style="background:rgba(37, 99, 235, 0.1); color:var(--color-primary); padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">คนขับประจำ</span>` : 
                    `<span style="background:rgba(139, 92, 246, 0.1); color:var(--color-secondary); padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:bold;">ขนส่งนอก</span>`;

                let weightCapacityHtml = '';
                if (drv.driverType === '3pl') {
                    const fixedW = drv.maxWeight || getDriverDefaultMaxWeight('3pl', drv.vehicleType);
                    weightCapacityHtml = `<span style="color:var(--hq-text-muted); font-weight:600;">${fixedW.toLocaleString()} กก. (คงที่)</span>`;
                } else {
                    const currentW = drv.maxWeight || getDriverDefaultMaxWeight('regular', drv.vehicleType);
                    weightCapacityHtml = `
                        <input type="number" class="table-input" value="${currentW}" 
                               style="width: 100px; padding: 4px 8px; border-radius: 8px; border: 1px solid var(--hq-border); background: rgba(255,255,255,0.03); color: white; text-align: center; font-weight: bold;" 
                               onchange="updateDriverMaxWeight('${drv.id}', this.value)">
                    `;
                }

                tbody.innerHTML += `
                    <tr>
                        <td style="font-family:var(--font-heading); font-weight:600;">${drv.id}</td>
                        <td>${typeLabel}</td>
                        <td><strong>${drv.name}</strong></td>
                        <td>${drv.phone}</td>
                        <td>${drv.plate}</td>
                        <td><strong>${drv.plateProvince || 'ไม่ระบุ'}</strong></td>
                        <td><span style="color: var(--color-secondary); font-weight: 600;">${drv.warehouse || 'สุขสวัสดิ์'}</span></td>
                        <td>${vehicleMapping[drv.vehicleType] || drv.vehicleType}</td>
                        <td>${weightCapacityHtml}</td>
                        <td>${statusBadge}</td>
                        <td><div style="display:flex; gap:0.5rem;">${actionBtn}</div></td>
                    </tr>
                `;
            });
        }

        function updateDriverMaxWeight(driverId, value) {
            const drivers = DB.get("drivers");
            const drv = drivers.find(d => d.id === driverId);
            if (drv) {
                const parsed = parseFloat(value);
                if (!isNaN(parsed) && parsed >= 0) {
                    drv.maxWeight = parsed;
                    DB.set("drivers", drivers);
                    // Refresh routing displays if any selected
                    if (typeof selectedAssignWarehouseName !== 'undefined' && selectedAssignWarehouseName) {
                        const activeWhBtn = document.querySelector(`.warehouse-sel-btn[data-wh="${selectedAssignWarehouseName}"]`);
                        selectAssignWarehouse(selectedAssignWarehouseName, activeWhBtn);
                    }
                } else {
                    alert("กรุณากรอกน้ำหนักบรรทุกที่ถูกต้อง!");
                    renderDriversTable();
                }
            }
        }"""

    if original_render_drivers_table in content:
        content = content.replace(original_render_drivers_table, new_render_drivers_table)
        print("  - renderDriversTable JS updated.")
    else:
        print("  - ERROR: original_render_drivers_table JS not found!")

    # 5. JS sheetJS parsing change in handleExcelFileUpload
    original_sheet_to_json = "const json = XLSX.utils.sheet_to_json(worksheet);"
    new_sheet_to_json = "const json = XLSX.utils.sheet_to_json(worksheet, { header: 'A' });"
    if original_sheet_to_json in content:
        content = content.replace(original_sheet_to_json, new_sheet_to_json)
        print("  - sheet_to_json with header A updated.")
    else:
        print("  - ERROR: original_sheet_to_json not found!")

    # 6. JS mapExcelJsonToOrders replacement
    original_map_excel = """        function mapExcelJsonToOrders(json) {
            const mapped = [];
            json.forEach(row => {
                const getRowVal = (keys) => {
                    for (let k of keys) {
                        if (row[k] !== undefined) return row[k];
                    }
                    return null;
                };

                const customerName = getRowVal(["ชื่อลูกค้า", "Customer Name", "customerName", "ร้านค้า"]);
                const lat = parseFloat(getRowVal(["ละติจูด", "Latitude", "lat", "lat"])) || null;
                const lng = parseFloat(getRowVal(["ลองจิจูด", "Longitude", "lng", "lng"])) || null;
                const cod = parseFloat(getRowVal(["ยอดเก็บเงิน", "COD Amount", "codAmount", "COD"])) || 0;
                const appt = getRowVal(["เวลานัดหมาย", "Appointment Time", "appointmentTime", "เวลานัด"]) || "09:00 - 11:00";
                const priority = getRowVal(["ความสำคัญ", "Priority", "priority"]) || "medium";
                const warehouse = getRowVal(["คลังสินค้า", "Warehouse", "warehouse", "คลัง"]) || "สุขสวัสดิ์";
                
                const itemLine = getRowVal(["รายการสินค้า", "สินค้า", "Items", "items"]);
                const parsedItems = parseExcelItemLine(itemLine);
                
                let totalWeight = 0;
                parsedItems.forEach(item => {
                    totalWeight += item.weight * item.qty;
                });

                if (customerName && lat && lng) {
                    mapped.push({
                        id: `ORD-${1000 + Math.floor(Math.random() * 9000)}`,
                        customerName,
                        address: `จุดนำเข้าไฟล์ (${lat.toFixed(4)}, ${lng.toFixed(4)})`,
                        lat,
                        lng,
                        items: parsedItems,
                        totalWeight: totalWeight,
                        codAmount: cod,
                        appointmentTime: appt,
                        priority: priority.toLowerCase(),
                        assignedDriverId: null,
                        routeSequence: 0,
                        status: 'pending',
                        warehouse,
                        createdAt: new Date().toISOString()
                    });
                }
            });
            return mapped;
        }"""

    new_map_excel = """        function mapExcelJsonToOrders(json) {
            const mapped = [];
            json.forEach(row => {
                // Determine keys matching A, B, C, D, I, T
                let id = row.A || row["stop_id"] || row["หมายเลขจุดส่ง หรือ ID ของกล่องสินค้า\\n(ห้ามซ้ำ)"] || row["ID"];
                let latVal = row.B || row["lat"] || row["ละติจูด ที่อยู่ที่จะจัดส่ง"] || row["ละติจูด"];
                let lngVal = row.C || row["lng"] || row["ลองจิจูด ที่อยู่ที่จะจัดส่ง"] || row["ลองจิจูด"];
                let customerName = row.D || row["customer_id"] || row["รหัสลูกค้า"] || row["ชื่อลูกค้า"];
                let weightVal = row.I || row["weight"] || row["น้ำหนักของสินค้าที่จะส่งที่จุดนี้"] || row["น้ำหนัก"];
                let note = row.T || row["note"] || row["บันทึก"] || row["หมายเหตุ"];

                if (id) id = String(id).trim();
                if (customerName) customerName = String(customerName).trim();
                if (note) note = String(note).trim();

                // Skip header rows
                if (id && (id.toLowerCase().includes("id") || id.includes("หมายเลข"))) return;
                if (customerName && (customerName.toLowerCase().includes("customer") || customerName.includes("ลูกค้า") || customerName.includes("รหัส"))) return;

                const lat = parseFloat(latVal);
                const lng = parseFloat(lngVal);
                const weight = parseFloat(weightVal) || 0;

                if (customerName && !isNaN(lat) && !isNaN(lng)) {
                    let orderType = 'delivery';
                    if (note && (note.includes("รับกลับ") || note.includes("คืนสินค้า") || note.includes("รับคืน") || note.includes("เก็บคืน"))) {
                        orderType = 'return';
                    }

                    mapped.push({
                        id: id || `ORD-${1000 + Math.floor(Math.random() * 9000)}`,
                        type: orderType,
                        customerName,
                        address: note ? `${customerName} (${note})` : `จุดนำเข้าไฟล์ (${lat.toFixed(4)}, ${lng.toFixed(4)})`,
                        lat,
                        lng,
                        items: [{ name: note || "สินค้าตามบิล Excel", weight: weight, qty: 1 }],
                        totalWeight: weight,
                        remarks: note || "",
                        codAmount: 0,
                        appointmentTime: "09:00 - 11:00",
                        priority: "medium",
                        assignedDriverId: null,
                        routeSequence: 0,
                        status: 'pending',
                        warehouse: selectedAssignWarehouseName || "สุขสวัสดิ์",
                        createdAt: new Date().toISOString()
                    });
                }
            });
            return mapped;
        }"""

    if original_map_excel in content:
        content = content.replace(original_map_excel, new_map_excel)
        print("  - mapExcelJsonToOrders JS updated.")
    else:
        print("  - ERROR: original_map_excel JS not found!")

    # 7. JS selectAssignWarehouse and selectAssignDriver updates
    original_select_wh = """            approvedDrivers.forEach(drv => {
                const driverOrders = orders.filter(o => o.assignedDriverId === drv.id);
                const activeJobs = driverOrders.filter(o => o.status !== 'success' && o.status !== 'failed').length;
                const totalJobs = driverOrders.length;
                const totalWeight = driverOrders.reduce((sum, o) => sum + (parseFloat(o.totalWeight) || 0), 0);
                
                const vehicleMappingShort = { pickup: "กระบะ", truck: "6ล้อ", truck_12: "12ล้อ", motorcycle: "มอเตอร์ไซค์" };
                const vehText = vehicleMappingShort[drv.vehicleType] || drv.vehicleType;
                
                driverListEl.innerHTML += `
                    <div class="driver-sel-card" data-drvid="${drv.id}" onclick="selectAssignDriver('${drv.id}', this)" style="margin-bottom: 0.4rem;">
                        <div>
                            <strong style="color: white; font-size: 0.9rem; display: block;">${drv.name}</strong>
                            <span style="font-size: 0.72rem; color: var(--hq-text-muted);">
                                📞 ${drv.phone || '-'} | 🚗 ${drv.plate || '-'} ${drv.plateProvince || ''}
                            </span>
                            <span class="payload-weight-text" style="font-size: 0.72rem; color: var(--color-primary); display: block; margin-top: 2px;">
                                ⚖️ บรรทุก: ${totalWeight.toLocaleString()} กก.
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 0.72rem; font-weight: 700; color: var(--color-secondary); display: block;">[${vehText}]</span>
                            <span class="jobs-count-text" style="font-size: 0.7rem; color: var(--hq-text-muted);">${activeJobs} งานค้าง / ${totalJobs} ทั้งหมด</span>
                        </div>
                    </div>
                `;
            });"""

    new_select_wh = """            approvedDrivers.forEach(drv => {
                const driverOrders = orders.filter(o => o.assignedDriverId === drv.id);
                const activeJobs = driverOrders.filter(o => o.status !== 'success' && o.status !== 'failed').length;
                const totalJobs = driverOrders.length;
                const totalWeight = driverOrders.reduce((sum, o) => sum + (parseFloat(o.totalWeight) || 0), 0);
                
                const vehicleMappingShort = { pickup: "กระบะ", truck: "6ล้อ", truck_12: "12ล้อ" };
                const vehText = vehicleMappingShort[drv.vehicleType] || drv.vehicleType;
                
                const maxW = drv.maxWeight || getDriverDefaultMaxWeight(drv.driverType || 'regular', drv.vehicleType);
                const isOverloaded = totalWeight > maxW;
                const weightColor = isOverloaded ? 'var(--color-danger)' : 'var(--color-primary)';
                const overloadWarning = isOverloaded ? ` <span style="color:var(--color-danger); font-weight:bold;">⚠️ เกินพิกัด!</span>` : '';

                driverListEl.innerHTML += `
                    <div class="driver-sel-card" data-drvid="${drv.id}" onclick="selectAssignDriver('${drv.id}', this)" style="margin-bottom: 0.4rem;">
                        <div>
                            <strong style="color: white; font-size: 0.9rem; display: block;">${drv.name}</strong>
                            <span style="font-size: 0.72rem; color: var(--hq-text-muted);">
                                📞 ${drv.phone || '-'} | 🚗 ${drv.plate || '-'} ${drv.plateProvince || ''}
                            </span>
                            <span class="payload-weight-text" style="font-size: 0.72rem; color: ${weightColor}; display: block; margin-top: 2px;">
                                ⚖️ บรรทุก: ${totalWeight.toLocaleString()} / ${maxW.toLocaleString()} กก.${overloadWarning}
                            </span>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-size: 0.72rem; font-weight: 700; color: var(--color-secondary); display: block;">[${vehText}]</span>
                            <span class="jobs-count-text" style="font-size: 0.7rem; color: var(--hq-text-muted);">${activeJobs} งานค้าง / ${totalJobs} ทั้งหมด</span>
                        </div>
                    </div>
                `;
            });"""

    if original_select_wh in content:
        content = content.replace(original_select_wh, new_select_wh)
        print("  - selectAssignWarehouse JS updated.")
    else:
        print("  - ERROR: original_select_wh not found!")

    original_select_drv = """            const activeCard = card || document.querySelector(`.driver-sel-card[data-drvid="${drvId}"]`);
            if (activeCard) {
                document.querySelectorAll('.driver-sel-card').forEach(c => c.classList.remove('active'));
                activeCard.classList.add('active');
                
                const payloadWeightEl = activeCard.querySelector('.payload-weight-text');
                if (payloadWeightEl) {
                    payloadWeightEl.textContent = `⚖️ บรรทุก: ${totalWeight.toLocaleString()} กก.`;
                }

                const jobsCountEl = activeCard.querySelector('.jobs-count-text');
                if (jobsCountEl) {
                    jobsCountEl.textContent = `${activeJobs} งานค้าง / ${totalJobs} ทั้งหมด`;
                }
            }"""

    new_select_drv = """            const activeCard = card || document.querySelector(`.driver-sel-card[data-drvid="${drvId}"]`);
            if (activeCard) {
                document.querySelectorAll('.driver-sel-card').forEach(c => c.classList.remove('active'));
                activeCard.classList.add('active');
                
                const drv = DB.get("drivers").find(d => d.id === drvId);
                const maxW = drv ? (drv.maxWeight || getDriverDefaultMaxWeight(drv.driverType || 'regular', drv.vehicleType)) : 2000;
                const isOverloaded = totalWeight > maxW;
                const weightColor = isOverloaded ? 'var(--color-danger)' : 'var(--color-primary)';
                const overloadWarning = isOverloaded ? ' ⚠️ เกินพิกัด!' : '';

                const payloadWeightEl = activeCard.querySelector('.payload-weight-text');
                if (payloadWeightEl) {
                    payloadWeightEl.textContent = `⚖️ บรรทุก: ${totalWeight.toLocaleString()} / ${maxW.toLocaleString()} กก.${overloadWarning}`;
                    payloadWeightEl.style.color = weightColor;
                }

                const jobsCountEl = activeCard.querySelector('.jobs-count-text');
                if (jobsCountEl) {
                    jobsCountEl.textContent = `${activeJobs} งานค้าง / ${totalJobs} ทั้งหมด`;
                }
            }"""

    if original_select_drv in content:
        content = content.replace(original_select_drv, new_select_drv)
        print("  - selectAssignDriver JS updated.")
    else:
        print("  - ERROR: original_select_drv not found!")

    # 8. Add extra helper scripts, excel handlers, and route transfer scripts
    new_js_logic = """
        // --- DRIVER EXCEL AND ROUTE TRANSFER EXTENSIONS ---
        let activeReportDriverId = null;

        function downloadSampleDriverCSV() {
            const csvRows = [
                ["รหัสระบบ", "ประเภทคนขับ", "ชื่อพนักงาน", "เบอร์โทรศัพท์", "เลขทะเบียน", "จังหวัดทะเบียน", "ประเภทพาหนะ", "น้ำหนักบรรทุกสูงสุด (กก.)", "คลังสินค้าที่รับงาน"],
                ["drv-1", "regular", "สมชาย ยอดขนส่ง (Somchai)", "081-234-5678", "1กข-9988", "กรุงเทพฯ", "pickup", "2200", "สุขสวัสดิ์"],
                ["drv-2", "regular", "วิชัย ใจดี (Wichai)", "089-876-5432", "3กน-4521", "ชลบุรี", "truck", "5500", "พัทยา"],
                ["", "3pl", "มานะ ขนส่งนอก (Mana)", "085-333-4444", "มข-789", "นครราชสีมา", "pickup", "3500", "โคราช"]
            ];
            
            // Format CSV with UTF-8 BOM
            const csvContent = "\\ufeff" + csvRows.map(e => e.join(",")).join("\\n");
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.setAttribute("download", "driver_template_sample.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function handleDriverExcelDrop(e) {
            e.preventDefault();
            this.style.borderColor = '';
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                const input = document.getElementById('driverExcelFileInput');
                input.files = files;
                handleDriverExcelUpload(input);
            }
        }

        function handleDriverExcelUpload(input) {
            const file = input.files[0];
            if (!file) return;

            const reader = new FileReader();
            const filename = file.name.toLowerCase();

            if (filename.endsWith('.csv')) {
                reader.onload = function(e) {
                    const text = e.target.result;
                    parseDriverCSV(text);
                };
                reader.readAsText(file, 'UTF-8');
            } else {
                reader.onload = function(e) {
                    const data = new Uint8Array(e.target.result);
                    try {
                        const workbook = XLSX.read(data, { type: 'array' });
                        const firstSheetName = workbook.SheetNames[0];
                        const worksheet = workbook.Sheets[firstSheetName];
                        const json = XLSX.utils.sheet_to_json(worksheet);
                        updateDriversFromExcel(json);
                    } catch(err) {
                        alert("เกิดข้อผิดพลาดในการโหลดไฟล์ Excel สำหรับคนขับ: " + err.message);
                    }
                };
                reader.readAsArrayBuffer(file);
            }
            
            input.value = '';
        }

        function parseDriverCSV(text) {
            const lines = text.split('\\n');
            if (lines.length < 2) {
                alert("ไฟล์ CSV ไม่มีข้อมูลเพียงพอ");
                return;
            }

            const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, '').replace(/^\\ufeff/, ''));
            const rows = [];

            const getVal = (rowValues, keyArray) => {
                for (const key of keyArray) {
                    const idx = headers.findIndex(h => h.toLowerCase() === key.toLowerCase() || h === key);
                    if (idx !== -1 && rowValues[idx] !== undefined) {
                        return rowValues[idx].trim().replace(/"/g, '');
                    }
                }
                return null;
            };

            for (let i = 1; i < lines.length; i++) {
                const line = lines[i].trim();
                if (!line) continue;
                
                const rowValues = line.split(',').map(v => v.trim());
                const id = getVal(rowValues, ["รหัสระบบ", "id", "Driver ID"]);
                const driverType = getVal(rowValues, ["ประเภทคนขับ", "type", "driverType", "Driver Type"]) || "regular";
                const name = getVal(rowValues, ["ชื่อพนักงาน", "name", "Name", "ชื่อ-นามสกุล"]);
                const phone = getVal(rowValues, ["เบอร์โทรศัพท์", "phone", "Phone"]);
                const plate = getVal(rowValues, ["เลขทะเบียน", "plate", "Plate"]);
                const plateProvince = getVal(rowValues, ["จังหวัดทะเบียน", "province", "plateProvince"]);
                const vehicleType = getVal(rowValues, ["ประเภทพาหนะ", "vehicleType", "vehicle"]) || "pickup";
                const maxWeight = getVal(rowValues, ["น้ำหนักบรรทุกสูงสุด (กก.)", "maxWeight", "capacity", "Max Capacity"]);
                const warehouse = getVal(rowValues, ["คลังสินค้าที่รับงาน", "warehouse", "Warehouse", "คลังสินค้า"]) || "สุขสวัสดิ์";

                if (name && plate) {
                    rows.push({ id, driverType, name, phone, plate, plateProvince, vehicleType, maxWeight, warehouse });
                }
            }
            updateDriversFromExcel(rows);
        }

        function updateDriversFromExcel(json) {
            if (!json || json.length === 0) {
                alert("ไม่พบข้อมูลคนขับในไฟล์ที่อัปโหลด");
                return;
            }

            const drivers = DB.get("drivers") || [];
            let updateCount = 0;
            let insertCount = 0;

            const getRowVal = (row, keys) => {
                for (let k of keys) {
                    if (row[k] !== undefined) return row[k];
                }
                return null;
            };

            json.forEach(row => {
                let id = getRowVal(row, ["รหัสระบบ", "id", "Driver ID", "ID"]);
                let driverType = getRowVal(row, ["ประเภทคนขับ", "driverType", "type"]) || "regular";
                let name = getRowVal(row, ["ชื่อพนักงาน", "name", "Name", "ชื่อ-นามสกุล"]);
                let phone = getRowVal(row, ["เบอร์โทรศัพท์", "phone", "Phone"]) || "";
                let plate = getRowVal(row, ["เลขทะเบียน", "plate", "Plate"]);
                let plateProvince = getRowVal(row, ["จังหวัดทะเบียน", "province", "plateProvince"]) || "กรุงเทพฯ";
                let vehicleType = getRowVal(row, ["ประเภทพาหนะ", "vehicleType", "vehicle"]) || "pickup";
                let maxWeightVal = getRowVal(row, ["น้ำหนักบรรทุกสูงสุด (กก.)", "maxWeight", "capacity", "Max Capacity"]);
                let warehouse = getRowVal(row, ["คลังสินค้าที่รับงาน", "warehouse", "Warehouse"]) || "สุขสวัสดิ์";

                if (id) id = String(id).trim();
                if (plate) plate = String(plate).trim();
                if (name) name = String(name).trim();

                // Skip header rows
                if (id && id.toLowerCase().includes("id")) return;
                if (name && (name.includes("ชื่อพนักงาน") || name.toLowerCase().includes("name"))) return;

                if (!name || !plate) return;

                // Match by ID or Plate
                let existing = null;
                if (id) {
                    existing = drivers.find(d => d.id === id);
                }
                if (!existing && plate) {
                    existing = drivers.find(d => d.plate === plate);
                }

                // If vehicleType is motorcycle, auto-migrate to pickup
                if (vehicleType === 'motorcycle') {
                    vehicleType = 'pickup';
                }

                let maxWeight = parseFloat(maxWeightVal);
                if (driverType === '3pl') {
                    maxWeight = getDriverDefaultMaxWeight('3pl', vehicleType);
                } else if (isNaN(maxWeight)) {
                    maxWeight = getDriverDefaultMaxWeight('regular', vehicleType);
                }

                if (existing) {
                    existing.name = name;
                    existing.phone = phone;
                    existing.plate = plate;
                    existing.plateProvince = plateProvince;
                    existing.vehicleType = vehicleType;
                    existing.maxWeight = maxWeight;
                    existing.warehouse = warehouse;
                    existing.driverType = driverType;
                    updateCount++;
                } else {
                    const newId = id || `drv-${Date.now()}-${Math.floor(Math.random()*1000)}`;
                    drivers.push({
                        id: newId,
                        name,
                        phone,
                        plate,
                        plateProvince,
                        vehicleType,
                        warehouse,
                        status: 'approved',
                        driverType,
                        maxWeight
                    });
                    insertCount++;
                }
            });

            DB.set("drivers", drivers);
            renderDriversTable();
            alert(`✅ นำเข้าข้อมูลคนขับสำเร็จ! (เพิ่มใหม่: ${insertCount} คน, อัปเดตข้อมูล: ${updateCount} คน)`);
        }

        function openQueueTransferQuick() {
            if (!selectedAssignDriverId) {
                alert("⚠️ กรุณาเลือกคนขับที่คุณต้องการโอนย้ายคิวงานจากรายการซ้ายมือก่อน!");
                return;
            }
            showDriverRouteReport(selectedAssignDriverId);
        }

        function executeRouteTransfer(sourceDriverId, targetDriverId, filterType) {
            if (!sourceDriverId || !targetDriverId) return;
            if (sourceDriverId === targetDriverId) {
                alert("⚠️ ไม่สามารถโอนเส้นทางไปยังคนขับคนเดิมได้!");
                return;
            }

            const allOrders = DB.get("orders");
            const drivers = DB.get("drivers");
            const targetDrv = drivers.find(d => d.id === targetDriverId);
            if (!targetDrv) return;

            // Get source driver pending orders
            let sourcePending = allOrders.filter(o => o.assignedDriverId === sourceDriverId && o.status !== 'success' && o.status !== 'failed');

            if (sourcePending.length === 0) {
                alert("❌ คนขับต้นทางไม่มีใบงานค้างจัดส่งที่สามารถโอนได้");
                return;
            }

            if (filterType === 'returns_only') {
                sourcePending = sourcePending.filter(o => o.type === 'return' || o.id.startsWith('RET-'));
                if (sourcePending.length === 0) {
                    alert("❌ ไม่พบงานรับสินค้ากลับ (Return Jobs) ในคิวงานของคนขับคนนี้");
                    return;
                }
            }

            const transferWeight = sourcePending.reduce((sum, o) => sum + (parseFloat(o.totalWeight) || 0), 0);
            
            // Calculate target driver's current pending weight
            const targetOrders = allOrders.filter(o => o.assignedDriverId === targetDriverId);
            const targetCurrentWeight = targetOrders.reduce((sum, o) => sum + (parseFloat(o.totalWeight) || 0), 0);
            const targetMaxWeight = targetDrv.maxWeight || getDriverDefaultMaxWeight(targetDrv.driverType || 'regular', targetDrv.vehicleType);

            if (targetCurrentWeight + transferWeight > targetMaxWeight) {
                const over = (targetCurrentWeight + transferWeight) - targetMaxWeight;
                const proceed = confirm(`⚠️ คำเตือน: น้ำหนักบรรทุกรวมของคนขับปลายทางจะเกินกำหนด!\\n\\n` +
                                        `- บรรทุกปัจจุบัน: ${targetCurrentWeight.toLocaleString()} กก.\\n` +
                                        `- โอนเพิ่ม: ${transferWeight.toLocaleString()} กก.\\n` +
                                        `- รวมบรรทุกหลังโอน: ${(targetCurrentWeight + transferWeight).toLocaleString()} กก.\\n` +
                                        `- พิกัดรถทะเบียนนี้รองรับ: ${targetMaxWeight.toLocaleString()} กก. (เกินกำหนด: ${over.toLocaleString()} กก.)\\n\\n` +
                                        `คุณต้องการยืนยันและบังคับโอนย้ายคิวงานนี้ใช่หรือไม่?`);
                if (!proceed) return;
            }

            // Transfer orders
            sourcePending.forEach(o => {
                o.assignedDriverId = targetDriverId;
                // Move order to the same warehouse as target driver or keep
                o.warehouse = targetDrv.warehouse;
            });

            // Re-sequence source driver's remaining orders
            let sourceRemaining = allOrders.filter(o => o.assignedDriverId === sourceDriverId);
            let sourceFinished = sourceRemaining.filter(o => o.status === 'success' || o.status === 'failed').sort((a,b) => a.routeSequence - b.routeSequence);
            let sourceNewPending = sourceRemaining.filter(o => o.status !== 'success' && o.status !== 'failed');
            let optimizedSource = optimizeRoutes(sourceNewPending, currentOptimizeMode);
            optimizedSource.forEach((ord, idx) => {
                ord.routeSequence = sourceFinished.length + idx + 1;
            });

            // Re-sequence target driver's orders
            let targetAll = allOrders.filter(o => o.assignedDriverId === targetDriverId);
            let targetFinished = targetAll.filter(o => o.status === 'success' || o.status === 'failed').sort((a,b) => a.routeSequence - b.routeSequence);
            let targetNewPending = targetAll.filter(o => o.status !== 'success' && o.status !== 'failed');
            let optimizedTarget = optimizeRoutes(targetNewPending, currentOptimizeMode);
            optimizedTarget.forEach((ord, idx) => {
                ord.routeSequence = targetFinished.length + idx + 1;
            });

            DB.set("orders", allOrders);

            // Trigger Map Draw and Dashboard refresh
            renderLiveDashboard();
            if (selectedAssignWarehouseName) {
                selectAssignWarehouse(selectedAssignWarehouseName, document.querySelector(`.warehouse-sel-btn[data-wh="${selectedAssignWarehouseName}"]`));
            }
            if (selectedAssignDriverId) {
                selectAssignDriver(selectedAssignDriverId);
            }

            alert(`✅ โอนย้ายคิวงานสำเร็จ! โอนย้ายสำเร็จจำนวน ${sourcePending.length} จุด ไปยัง ${targetDrv.name}`);
        }

        function executeRouteTransferFromModal() {
            const targetSelect = document.getElementById('transferTargetDriverSelect');
            const typeSelect = document.getElementById('transferTypeSelect');
            if (!targetSelect || !typeSelect) return;

            const targetDriverId = targetSelect.value;
            const filterType = typeSelect.value;

            if (!targetDriverId) {
                alert("กรุณาเลือกคนขับปลายทางที่ต้องการโอนย้ายคิวงาน!");
                return;
            }

            executeRouteTransfer(activeReportDriverId, targetDriverId, filterType);
            hideDriverRouteReportModal();
        }
        """

    # In showDriverRouteReport modal setup, add activeReportDriverId assignment and target dropdown population
    original_show_report_start = """        function showDriverRouteReport(driverId) {
            const drivers = DB.get("drivers");
            const orders = DB.get("orders");
            const locations = DB.get("driverLocations");
            const drv = drivers.find(d => d.id === driverId);
            if (!drv) return;"""

    new_show_report_start = """        function showDriverRouteReport(driverId) {
            activeReportDriverId = driverId; // Set current report driver ID
            const drivers = DB.get("drivers");
            const orders = DB.get("orders");
            const locations = DB.get("driverLocations");
            const drv = drivers.find(d => d.id === driverId);
            if (!drv) return;

            // Populate transfer target driver dropdown
            const transferSelect = document.getElementById('transferTargetDriverSelect');
            if (transferSelect) {
                transferSelect.innerHTML = '';
                const otherDrivers = drivers.filter(d => d.status === 'approved' && d.id !== driverId);
                if (otherDrivers.length === 0) {
                    transferSelect.innerHTML = '<option value="">ไม่มีคนขับอื่นที่จะโอนคิวงานให้</option>';
                } else {
                    otherDrivers.forEach(d => {
                        const is3pl = d.driverType === '3pl';
                        const typeText = is3pl ? 'ขนส่งนอก' : 'ประจำ';
                        const plateInfo = `${d.plate} ${d.plateProvince || ''}`;
                        const cap = d.maxWeight || getDriverDefaultMaxWeight(d.driverType || 'regular', d.vehicleType);
                        transferSelect.innerHTML += `<option value="${d.id}">${d.name} (${typeText} - ${plateInfo}) [Max: ${cap} กก.]</option>`;
                    });
                }
            }"""

    if original_show_report_start in content:
        content = content.replace(original_show_report_start, new_show_report_start)
        print("  - showDriverRouteReport JS updated (populating target dropdown).")
    else:
        print("  - ERROR: original_show_report_start not found!")

    # Now append the new JS logic right before the closing </script> tag
    original_closing_script = "    </script>\n</body>\n</html>"
    new_closing_script = new_js_logic + "\n    </script>\n</body>\n</html>"
    if original_closing_script in content:
        content = content.replace(original_closing_script, new_closing_script)
        print("  - new JS helpers appended.")
    else:
        print("  - ERROR: original_closing_script not found!")

    # Remove motorcycle from mapping
    content = content.replace('motorcycle: "จักรยานยนต์ (Motorcycle)"', '')
    content = content.replace('motorcycle: "มอเตอร์ไซค์"', '')

    with open("admin.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("admin.html modification complete!")

def modify_driver_html():
    print("Modifying driver.html...")
    with open("driver.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Remove motorcycle select option
    content = content.replace('<option value="motorcycle">รถจักรยานยนต์ (Motorcycle)</option>', '')
    
    with open("driver.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("driver.html modification complete!")

def modify_super_html():
    print("Modifying super.html...")
    with open("super.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update the table header to include Max Capacity
    original_header = """                                    <th>คลังสังกัด</th>
                                    <th>ประเภทรถ</th>
                                    <th>สถานะสิทธิ์</th>"""
    
    new_header = """                                    <th>คลังสังกัด</th>
                                    <th>ประเภทรถ</th>
                                    <th>น้ำหนักบรรทุกสูงสุด (Max Capacity)</th>
                                    <th>สถานะสิทธิ์</th>"""

    if original_header in content:
        content = content.replace(original_header, new_header)
        print("  - super table header updated.")
    else:
        print("  - ERROR: original_header in super.html not found!")

    # 2. Update renderSuperDriversTable to display capacity and input fields
    original_render_super = """                tbody.innerHTML += `
                    <tr>
                        <td style="font-family:var(--font-heading); color:var(--hq-text-muted); font-size:0.8rem;">${drv.id}</td>
                        <td>${typeBadge}</td>
                        <td><strong>${drv.name}</strong></td>
                        <td>${drv.phone}</td>
                        <td><strong style="color:white;">${drv.plate}</strong></td>
                        <td>${drv.plateProvince || 'ไม่ระบุ'}</td>
                        <td><span style="font-weight:600; color:var(--color-secondary);">คลัง${drv.warehouse || 'สุขสวัสดิ์'}</span></td>
                        <td>${vehicleMapping[drv.vehicleType] || drv.vehicleType}</td>
                        <td><span class="super-status-badge ${badgeClass}">${statusText}</span></td>"""

    new_render_super = """                let weightCapacityHtml = '';
                if (drv.driverType === '3pl') {
                    const fixedW = drv.maxWeight || getDriverDefaultMaxWeight('3pl', drv.vehicleType);
                    weightCapacityHtml = `<span style="color:var(--hq-text-muted); font-weight:600;">${fixedW.toLocaleString()} กก. (คงที่)</span>`;
                } else {
                    const currentW = drv.maxWeight || getDriverDefaultMaxWeight('regular', drv.vehicleType);
                    weightCapacityHtml = `
                        <input type="number" class="table-input" value="${currentW}" 
                               style="width: 100px; padding: 4px 8px; border-radius: 8px; border: 1px solid var(--hq-border); background: rgba(255,255,255,0.03); color: white; text-align: center; font-weight: bold;" 
                               onchange="updateDriverMaxWeightFromSuper('${drv.id}', this.value)">
                    `;
                }

                tbody.innerHTML += `
                    <tr>
                        <td style="font-family:var(--font-heading); color:var(--hq-text-muted); font-size:0.8rem;">${drv.id}</td>
                        <td>${typeBadge}</td>
                        <td><strong>${drv.name}</strong></td>
                        <td>${drv.phone}</td>
                        <td><strong style="color:white;">${drv.plate}</strong></td>
                        <td>${drv.plateProvince || 'ไม่ระบุ'}</td>
                        <td><span style="font-weight:600; color:var(--color-secondary);">คลัง${drv.warehouse || 'สุขสวัสดิ์'}</span></td>
                        <td>${vehicleMapping[drv.vehicleType] || drv.vehicleType}</td>
                        <td>${weightCapacityHtml}</td>
                        <td><span class="super-status-badge ${badgeClass}">${statusText}</span></td>"""

    if original_render_super in content:
        content = content.replace(original_render_super, new_render_super)
        print("  - renderSuperDriversTable JS rendering updated.")
    else:
        print("  - ERROR: original_render_super not found!")

    # 3. Add JS helper updateDriverMaxWeightFromSuper and remove motorcycle
    new_super_js = """
        function updateDriverMaxWeightFromSuper(driverId, value) {
            const drivers = DB.get("drivers", []);
            const drv = drivers.find(d => d.id === driverId);
            if (drv) {
                const parsed = parseFloat(value);
                if (!isNaN(parsed) && parsed >= 0) {
                    drv.maxWeight = parsed;
                    DB.set("drivers", drivers);
                    alert("บันทึกค่าน้ำหนักบรรทุกสูงสุดเรียบร้อย!");
                } else {
                    alert("กรุณากรอกน้ำหนักบรรทุกที่ถูกต้อง!");
                    renderSuperDriversTable();
                }
            }
        }
    """

    original_closing_super = "    </script>\n</body>\n</html>"
    new_closing_super = new_super_js + "\n    </script>\n</body>\n</html>"
    if original_closing_super in content:
        content = content.replace(original_closing_super, new_closing_super)
        print("  - new Super JS helpers appended.")
    else:
        print("  - ERROR: original_closing_super not found!")

    # Remove motorcycle options
    content = content.replace('<option value="motorcycle">รถมอเตอร์ไซค์ (Motorcycle)</option>', '')
    content = content.replace('motorcycle: "จักรยานยนต์ (Motorcycle)"', '')

    with open("super.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("super.html modification complete!")

if __name__ == "__main__":
    modify_admin_html()
    modify_driver_html()
    modify_super_html()
    print("All files updated successfully!")
