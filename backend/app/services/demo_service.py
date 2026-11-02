import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.ingestion.zip_processor import SecureZipProcessor
from app.core.logging import log_pipeline_event

class DemoBusinessService:
    """Discovers synthetic business ZIPs dynamically from data/demo-businesses/ and manages demo environments."""

    @classmethod
    def get_demo_dir(cls) -> Path:
        """Resolve directory containing demo business archives."""
        p = settings.DEMO_BUSINESSES_DIR
        if not p.exists():
            # Alternative relative fallback
            alt = Path(__file__).resolve().parent.parent.parent.parent / "data" / "demo-businesses"
            if alt.exists():
                return alt
        return p

    @classmethod
    def discover_all_demo_businesses(cls) -> List[Dict[str, Any]]:
        """Dynamically scan data/demo-businesses/ for all .zip archives and read their company.json."""
        demo_dir = cls.get_demo_dir()
        businesses: List[Dict[str, Any]] = []

        if not demo_dir.exists():
            return []

        zip_files = sorted(list(demo_dir.glob("*.zip")))
        for zpath in zip_files:
            try:
                info = SecureZipProcessor.inspect_zip(zpath)
                meta = info.get("company_metadata", {})
                
                # Derive slug/id
                company_name = meta.get("company") or meta.get("company_name") or zpath.stem.replace("_Aegis_Demo", "")
                slug = meta.get("slug") or company_name.lower().replace(" ", "")
                industry = meta.get("industry") or "Enterprise Commerce"
                
                # Clean industry title
                formatted_industry = industry.replace("_", " ").title()
                
                businesses.append({
                    "id": slug,
                    "name": company_name,
                    "industry": formatted_industry,
                    "tagline": meta.get("description", f"Enterprise {formatted_industry} intelligence environment"),
                    "description": meta.get("description", f"Synthetic multi-dataset enterprise twin for {company_name}."),
                    "zipFileName": zpath.name,
                    "datasetCount": info["dataset_count"],
                    "recordCount": max(42000, info["dataset_count"] * 38000),
                    "healthScore": 78 if slug == "primelogix" else 74,
                    "riskCount": 4 if slug == "primelogix" else 3,
                    "primaryRiskStory": {
                        "trigger": f"Operational & macro volatility signals detected across {formatted_industry} supply corridors",
                        "causalChain": ["Benchmark Price Variance", "Margin Compression", "SLA Deviation", "Capital Exposure"],
                        "affectedMetrics": ["Gross Operating Margin", "Cash Flow Run Rate", "SLA Compliance"],
                        "potentialImpact": "$2.85M annualized exposure",
                    },
                    "metrics": {
                        "revenue": "$148.2M",
                        "growth": "+8.4%",
                        "margin": "14.2%",
                        "runway": "18 mo",
                    },
                })
            except Exception as e:
                log_pipeline_event("DEMO_DISCOVERY_ERROR", f"Could not inspect {zpath.name}: {str(e)}")

        return businesses

    @classmethod
    def get_business_by_id(cls, business_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single discovered business by slug or id."""
        all_b = cls.discover_all_demo_businesses()
        for b in all_b:
            if b["id"].lower() == business_id.lower() or b["name"].lower() == business_id.lower():
                return b
        if all_b:
            return all_b[0]
        return None
