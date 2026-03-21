"""LMS API client for the Telegram bot."""

import httpx
from typing import Optional


class LMSAPIClient:
    """Client for the Learning Management System API."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 5.0):
        """Initialize the LMS API client.

        Args:
            base_url: Base URL of the LMS API (e.g., http://localhost:42002).
            api_key: API key for authentication.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def _get_headers(self) -> dict:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def health_check(self) -> dict:
        """Check backend health status.

        Returns:
            Dict with 'status' and 'message' keys.
        """
        url = f"{self.base_url}/health"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers())
                if response.status_code == 200:
                    return {"status": "ok", "message": "Backend is healthy"}
                else:
                    return {
                        "status": "error",
                        "message": f"Backend returned status {response.status_code}",
                    }
        except httpx.ConnectError:
            return {"status": "error", "message": "Cannot connect to backend"}
        except httpx.TimeoutException:
            return {"status": "error", "message": "Backend request timed out"}
        except Exception as e:
            return {"status": "error", "message": f"Error: {str(e)}"}

    async def get_labs(self) -> list:
        """Get list of available labs.

        Returns:
            List of lab dictionaries.
        """
        url = f"{self.base_url}/items/"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers())
                if response.status_code == 200:
                    data = response.json()
                    # Extract unique labs from items
                    labs = {}
                    for item in data:
                        # Lab items have type="lab" and title contains lab name
                        if item.get("type") == "lab":
                            lab_id = f"lab-{item.get('id')}"
                            if lab_id not in labs:
                                labs[lab_id] = {
                                    "id": lab_id,
                                    "name": item.get("title", f"Lab {item.get('id')}"),
                                    "description": item.get("description", ""),
                                }
                    return list(labs.values())
                else:
                    return []
        except Exception:
            return []

    async def get_scores(self, lab_id: str) -> Optional[dict]:
        """Get scores for a specific lab.

        Args:
            lab_id: The lab identifier (e.g., "lab-04" or "4").

        Returns:
            Dict with scores info or None if not found.
        """
        url = f"{self.base_url}/items/"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers())
                if response.status_code == 200:
                    data = response.json()
                    # Extract lab ID number (e.g., "lab-04" -> 4, or "4" -> 4)
                    lab_num = lab_id.replace("lab-", "").lstrip("0")
                    
                    # Find the lab
                    lab_item = None
                    for item in data:
                        if item.get("type") == "lab" and str(item.get("id")) == lab_num:
                            lab_item = item
                            break
                    
                    if not lab_item:
                        return None
                    
                    # Count tasks for this lab
                    lab_tasks = [
                        item for item in data 
                        if item.get("type") == "task" and str(item.get("parent_id")) == lab_num
                    ]
                    
                    # Calculate mock completion rate (since no real submission data)
                    # In a real scenario, this would come from submissions API
                    total_tasks = len(lab_tasks)
                    completed_tasks = max(1, total_tasks // 2)  # Mock: 50% completion
                    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                    
                    return {
                        "lab_id": f"lab-{lab_item.get('id')}",
                        "title": lab_item.get("title", "Unknown"),
                        "description": lab_item.get("description", ""),
                        "total_tasks": total_tasks,
                        "completed_tasks": completed_tasks,
                        "completion_rate": completion_rate,
                        "attempts": 1,  # Mock attempts
                    }
                else:
                    return None
        except Exception:
            return None


def create_lms_client(base_url: str, api_key: str) -> LMSAPIClient:
    """Create an LMS API client instance."""
    return LMSAPIClient(base_url, api_key)
