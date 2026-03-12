from datetime import datetime
from sqlmodel import Session

from file_processing_api.db.database import engine
from file_processing_api.db.models import Archive, File


def add_sample_data():
    with Session(engine) as session:
        archive = Archive(filename="my_archive.zip", uploaded_at=datetime.utcnow())
        session.add(archive)
        session.commit()
        session.refresh(archive)

        file = File(
            archive_id=archive.id,
            filename="file1.txt",
            content="Hello, world!"
        )
        session.add(file)

        session.commit()
        print(f"Inserted archive id={archive.id} and file id={file.id}")

if __name__ == "__main__":
    add_sample_data()