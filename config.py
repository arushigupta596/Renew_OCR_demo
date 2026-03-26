"""
Column mappings and configuration for each case tracker.
Maps semantic field names to Excel column numbers (1-indexed).
Row 5 = headers, data starts at row 6.
"""

DATA_START_ROW = 6
TEMPLATE_FILE = "Tracker_Format.xlsx"

# Sheet names per case
SHEET_NAMES = {
    1: "Case1_Tracker",
    2: "Case2_Tracker",
    3: "Case3_Tracker",
}

# Case descriptions
CASE_DESCRIPTIONS = {
    1: "Import - Purchase & Custom Clearance by EPC followed by Domestic Sale to SPV, Delivery to Site",
    2: "Import - Purchase by EPC, HSS to SPV, Custom Clearance by SPV, Delivery to Site",
    3: "Domestic - Purchase by EPC, Domestic Sale to SPV, Delivery to Site",
}

# Document types expected per case
EXPECTED_DOCUMENTS = {
    1: [
        "commercial_invoice",
        "packing_list",
        "certificate_of_origin",
        "bill_of_lading",
        "bill_of_entry",
        "duty_challan",
        "eway_bill",
        "tax_invoice",
        "einvoice",
        "lr_receipt",
        "grn",
    ],
    2: [
        "commercial_invoice",
        "packing_list",
        "certificate_of_origin",
        "hss_invoice",
        "hss_agreement",
        "bill_of_lading",
        "bill_of_entry",
        "duty_challan",
        "eway_bill",
        "lr_receipt",
        "grn",
    ],
    3: [
        "commercial_invoice",
        "packing_list",
        "eway_bill",
        "tax_invoice",
        "einvoice",
        "lr_receipt",
        "grn",
    ],
}

# ============================================================
# CASE 1 COLUMN MAPPING
# ============================================================
CASE1_COLUMNS = {
    # Section: Commercial Invoice Details (Supplier to EPC Sale)
    "s_no": 2,
    "commercial_invoice_no": 3,
    "ci_item_description": 4,
    "ci_date": 5,
    "ci_bill_to": 6,
    "ci_ship_to": 7,
    "ci_quantity": 8,
    "packing_list_available": 9,        # Yes/No
    "certificate_of_origin_available": 10,  # Yes/No
    "invoice_no_on_packing_list": 11,
    "invoice_no_on_certificate": 12,

    # Section: BoE Details
    "bl_available": 13,                 # Yes/No
    "bl_number": 14,
    "invoice_no_on_bl": 15,
    "boe_available": 16,                # Yes/No
    "boe_number": 17,
    "boe_item_description": 18,
    "boe_date": 19,
    "boe_quantity": 20,
    "boe_assessable_amount": 21,
    "bcd_amount": 22,
    "add_amount": 23,
    "boe_igst_amount": 24,
    "duty_challan_number": 25,
    "duty_challan_available": 26,       # Yes/No
    "boe_ci_number_linkage": 27,
    "boe_seller_name_address": 28,
    "boe_buyer_name_address": 29,

    # Section: Detailed E-way Bill Details
    "eway_bill_no": 30,
    "eway_boe_number_linkage": 31,
    "eway_generated_by": 32,
    "eway_generated_by_gstin": 33,
    "eway_item_description": 34,
    "eway_quantity": 35,
    "eway_type": 36,                    # Detailed/Normal
    "eway_bill_from": 37,
    "eway_ship_from": 38,
    "eway_bill_to": 39,
    "eway_ship_to": 40,
    "eway_taxable_value": 41,
    "eway_gst_amount": 42,
    "eway_total_value": 43,

    # Section: Tax Invoice Details (EPC to SPV Sale)
    "tax_invoice_no": 44,
    "ti_item_description": 45,
    "ti_bill_from": 46,
    "ti_bill_to": 47,
    "ti_ship_to": 48,
    "ti_place_of_supply": 49,
    "ti_irn_available": 50,             # Yes/No
    "ti_date": 51,
    "ti_quantity": 52,
    "ti_gst_rate": 53,
    "ti_taxable_value": 54,
    "ti_gst_amount": 55,
    "ti_tcs": 56,
    "ti_invoice_value": 57,
    "ti_einvoice_available": 58,        # Yes/No
    "ti_remarks": 59,

    # Col 60 is gap

    # Section: Transportation/Delivery Documentation
    "lr_available": 61,                 # Yes/No
    "lr_container_number": 62,
    "lr_invoice_ref_linkage": 63,
    "lr_eway_ref_linkage": 64,
    "lr_vehicle_no": 65,
    "lr_number": 66,
    "lr_date": 67,
    "lr_transporter_name": 68,
    "lr_consignee": 69,
    "gate_entry_no": 70,
    "gate_inward_date": 71,
    "gate_stamp": 72,                   # Yes/No
    "grn_available": 73,                # Yes/No
    "grn_invoice_no": 74,
    "grn_eway_bill_no": 75,
    "grn_vehicle_no": 76,
}

# ============================================================
# CASE 2 COLUMN MAPPING
# ============================================================
CASE2_COLUMNS = {
    # Section: Commercial Invoice Details (Supplier to EPC Sale)
    "s_no": 2,
    "commercial_invoice_no": 3,
    "ci_item_description": 4,
    "ci_date": 5,
    "ci_bill_to": 6,
    "ci_ship_to": 7,
    "ci_quantity": 8,
    "packing_list_available": 9,
    "certificate_of_origin_available": 10,
    "invoice_no_on_packing_list": 11,
    "invoice_no_on_certificate": 12,

    # Section: HSS Invoice (EPC to SPV)
    "hss_invoice_number": 13,
    "hss_item_description": 14,
    "hss_bill_from": 15,
    "hss_bill_to": 16,
    "hss_ship_to": 17,
    "hss_place_of_supply": 18,
    "hss_invoice_date": 19,
    "hss_invoice_quantity": 20,
    "hss_invoice_value": 21,

    # Section: HSS Agreement (EPC to SPV)
    "hss_agreement_number": 22,
    "hss_agreement_item_description": 23,
    "hss_invoice_no_in_agreement": 24,
    "hss_supplier_invoice_in_agreement": 25,
    "hss_bl_number_in_agreement": 26,
    "hss_buyer_name_in_agreement": 27,

    # Section: BoE Details (Custom Clearance by SPV)
    "bl_available": 28,
    "bl_number": 29,
    "invoice_no_on_bl": 30,
    "boe_available": 31,
    "boe_number": 32,
    "boe_item_description": 33,
    "boe_date": 34,
    "boe_quantity": 35,
    "boe_assessable_amount": 36,
    "bcd_amount": 37,
    "add_amount": 38,
    "boe_igst_amount": 39,
    "duty_challan_number": 40,
    "duty_challan_available": 41,
    "boe_ci_number_linkage": 42,
    "boe_seller_name_address": 43,
    "boe_buyer_name_address": 44,

    # Section: Detailed E-way Bill Details
    "eway_bill_no": 45,
    "eway_boe_number_linkage": 46,
    "eway_generated_by": 47,
    "eway_generated_by_gstin": 48,
    "eway_item_description": 49,
    "eway_quantity": 50,
    "eway_type": 51,
    "eway_bill_from": 52,
    "eway_ship_from": 53,
    "eway_bill_to": 54,
    "eway_ship_to": 55,
    "eway_taxable_value": 56,
    "eway_gst_amount": 57,
    "eway_total_value": 58,

    # Col 59 is gap

    # Section: Transportation/Delivery Documentation
    "lr_available": 60,
    "lr_container_number": 61,
    "lr_invoice_ref_linkage": 62,
    "lr_eway_ref_linkage": 63,
    "lr_vehicle_no": 64,
    "lr_number": 65,
    "lr_date": 66,
    "lr_transporter_name": 67,
    "lr_consignee": 68,
    "gate_entry_no": 69,
    "gate_inward_date": 70,
    "gate_stamp": 71,
    "grn_available": 72,
    "grn_invoice_no": 73,
    "grn_eway_bill_no": 74,
    "grn_vehicle_no": 75,
}

# ============================================================
# CASE 3 COLUMN MAPPING
# ============================================================
CASE3_COLUMNS = {
    # Section: Commercial Invoice Details (Supplier to EPC Sale) - actually first Tax Invoice
    "s_no": 2,
    "commercial_invoice_no": 3,
    "ci_item_description": 4,
    "ci_bill_from": 5,
    "ci_bill_to": 6,
    "ci_ship_to": 7,
    "ci_place_of_supply": 8,
    "ci_irn_available": 9,              # Yes/No
    "ci_date": 10,
    "ci_quantity": 11,
    "ci_gst_rate": 12,
    "ci_taxable_value": 13,
    "ci_gst_amount": 14,
    "ci_tcs": 15,
    "ci_invoice_value": 16,
    "packing_list_available": 17,       # Yes/No
    "ci_einvoice_available": 18,        # Yes/No
    "invoice_no_on_packing_list": 19,

    # Section: Detailed E-way Bill Details
    "eway_bill_no": 20,
    "eway_invoice_number_linkage": 21,
    "eway_generated_by": 22,
    "eway_generated_by_gstin": 23,
    "eway_item_description": 24,
    "eway_quantity": 25,
    "eway_type": 26,
    "eway_bill_from": 27,
    "eway_ship_from": 28,
    "eway_bill_to": 29,
    "eway_ship_to": 30,
    "eway_taxable_value": 31,
    "eway_gst_amount": 32,
    "eway_total_value": 33,

    # Section: Tax Invoice (EPC to SPV) - second Tax Invoice
    "tax_invoice_no": 34,
    "ti_item_description": 35,
    "ti_bill_from": 36,
    "ti_bill_to": 37,
    "ti_ship_to": 38,
    "ti_place_of_supply": 39,
    "ti_irn_available": 40,             # Yes/No
    "ti_date": 41,
    "ti_quantity": 42,
    "ti_gst_rate": 43,
    "ti_taxable_value": 44,
    "ti_gst_amount": 45,
    "ti_tcs": 46,
    "ti_invoice_value": 47,
    "ti_einvoice_available": 48,        # Yes/No
    "ti_remarks": 49,

    # Col 50 is gap

    # Section: Transportation/Delivery Documentation
    "lr_available": 51,
    "lr_container_number": 52,
    "lr_invoice_ref_linkage": 53,
    "lr_eway_ref_linkage": 54,
    "lr_vehicle_no": 55,
    "lr_number": 56,
    "lr_date": 57,
    "lr_transporter_name": 58,
    "lr_consignee": 59,
    "gate_entry_no": 60,
    "gate_inward_date": 61,
    "gate_stamp": 62,
    "grn_available": 63,
    "grn_invoice_no": 64,
    "grn_eway_bill_no": 65,
    "grn_vehicle_no": 66,
}

# Unified accessor
COLUMN_MAPPINGS = {
    1: CASE1_COLUMNS,
    2: CASE2_COLUMNS,
    3: CASE3_COLUMNS,
}

# Fields that should be extracted as JSON keys from the LLM
# These match the keys in the CASE*_COLUMNS dicts (excluding s_no)
def get_extraction_fields(case_number: int) -> list[str]:
    """Return list of field names to extract for a given case."""
    cols = COLUMN_MAPPINGS[case_number]
    return [k for k in cols.keys() if k != "s_no"]


# Default OpenRouter models
OPENROUTER_MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-2.5-pro-preview",
    "anthropic/claude-sonnet-4",
    "meta-llama/llama-4-maverick",
    "deepseek/deepseek-chat-v3-0324",
]
