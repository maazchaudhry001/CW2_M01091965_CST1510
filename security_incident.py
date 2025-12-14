class SecurityIncident:
    """Model representing a cybersecurity incident within the platform."""

    def __init__(
        self,
        incident_id: int,
        category: str,
        severity: str,
        status: str,
        description: str,
    ):
        self.__incident_id = incident_id
        self.__category = category
        self.__severity = severity
        self.__status = status
        self.__description = description

    def get_incident_id(self) -> int:
        return self.__incident_id

    def get_severity(self) -> str:
        return self.__severity

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description

    def update_status(self, status: str) -> None:
        """Update the current status of the incident."""
        self.__status = status

    def severity_level(self) -> int:
        """Convert severity label into a numeric severity level."""
        severity_map = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return severity_map.get(self.__severity.lower(), 0)

    def __str__(self) -> str:
        return (
            f"Incident {self.__incident_id} "
            f"[{self.__severity.upper()}] "
            f"{self.__category} - {self.__status}"
        )
