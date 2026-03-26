"""
File storage handler for organizing documents by category.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Storage:
    """Handles file storage operations for the PPP app."""

    def __init__(self, base_path: str = "data/documents"):
        """Initialize storage base path."""
        self.base_path = Path(base_path)

    def _ensure_category_dir(self, category: str) -> Path:
        """Create category directory if it doesn't exist."""
        category_path = self.base_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        return category_path

    def save_file(self, source_path: str, category: str, original_name: str) -> str:
        """
        Save an uploaded file to the appropriate category folder.

        Args:
            source_path: Temporary path of uploaded file
            category: Document category (determines subfolder)
            original_name: Original filename from upload

        Returns:
            The final storage path (relative to base_path)
        """
        category_dir = self._ensure_category_dir(category)

        # Generate new filename: YYYY-MM-DD_originalname
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        new_filename = f"{date_prefix}_{original_name}"
        destination = category_dir / new_filename

        # Handle duplicate filenames
        counter = 1
        while destination.exists():
            stem, ext = os.path.splitext(original_name)
            new_filename = f"{date_prefix}_{stem}_{counter}{ext}"
            destination = category_dir / new_filename
            counter += 1

        # Copy file to destination
        import shutil
        shutil.copy2(source_path, destination)

        # Return relative path
        return str(destination.relative_to(self.base_path))

    def get_full_path(self, relative_path: str) -> str:
        """Get absolute file path from relative storage path."""
        return str(self.base_path / relative_path)
