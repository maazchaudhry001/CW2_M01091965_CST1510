class Dataset:
    """Model representing a data science dataset within the platform."""

    def __init__(
        self,
        dataset_id: int,
        name: str,
        size_bytes: int,
        row_count: int,
        origin: str,
    ):
        self.__dataset_id = dataset_id
        self.__name = name
        self.__size_bytes = size_bytes
        self.__row_count = row_count
        self.__origin = origin

    def size_in_mb(self) -> float:
        """Return the dataset size in megabytes."""
        return self.__size_bytes / (1024 * 1024)

    def get_origin(self) -> str:
        return self.__origin

    def __str__(self) -> str:
        return (
            f"Dataset {self.__dataset_id}: {self.__name} "
            f"({self.size_in_mb():.2f} MB, "
            f"{self.__row_count} rows, source={self.__origin})"
        )
