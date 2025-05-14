# clone_and_rebind_powerbi.py

"""
Clone a semantic model and Power BI report, then rebind the cloned report to the new model.
Requires: semantic-link-labs
"""

!pip install semantic-link-labs --quiet

import sempy_labs as labs
import re

# ---------- Helpers ----------

def extract_dataset_ids(url):
    """Extract workspace and dataset ID from a Power BI dataset URL."""
    match = re.search(r"groups/([a-f0-9-]+)/datasets/([a-f0-9-]+)", url)
    if not match:
        raise ValueError("Invalid dataset URL.")
    return match.group(1), match.group(2)

def extract_report_ids(url):
    """Extract workspace and report ID from a Power BI report URL."""
    match = re.search(r"groups/([a-f0-9-]+)/reports/([a-f0-9-]+)", url)
    if not match:
        raise ValueError("Invalid report URL.")
    return match.group(1), match.group(2)

# ---------- Config ----------

dataset_url = "https://app.powerbi.com/groups/{workspaceId}/datasets/{datasetId}/details"
report_url = "https://app.powerbi.com/groups/{workspaceId}/reports/{reportId}"
target_dataset_name = "Semantic_Model_Meta_Data_Analyzer_SM"
cloned_report_name = "Cloned Report - Dev"

# ---------- Step 1: Clone Semantic Model ----------

try:
    source_workspace, source_dataset = extract_dataset_ids(dataset_url)

    labs.deploy_semantic_model(
        source_dataset=source_dataset,
        source_workspace=source_workspace,
        target_dataset=target_dataset_name,
        target_workspace=source_workspace,
        refresh_target_dataset=True,
        overwrite=False
    )

    print("✅ Semantic model cloned successfully.")

except Exception as e:
    print(f"❌ Error cloning semantic model: {e}")

# ---------- Step 2: Clone Report ----------

try:
    report_workspace, report_id = extract_report_ids(report_url)

    labs.report.clone_report(
        report=report_id,
        cloned_report=cloned_report_name,
        workspace=report_workspace,
        target_workspace=report_workspace
    )

    print("✅ Report cloned successfully.")

except Exception as e:
    print(f"❌ Error cloning report: {e}")

# ---------- Step 3: Rebind Report ----------

try:
    labs.report.report_rebind(
        report=cloned_report_name,
        dataset=target_dataset_name,
        report_workspace=report_workspace,
        dataset_workspace=source_workspace
    )

    print("✅ Report rebound to new dataset successfully.")

except Exception as e:
    print(f"❌ Error rebinding report: {e}")
