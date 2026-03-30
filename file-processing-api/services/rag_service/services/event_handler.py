from services.api_service.services.file_service import get_files_by_archive_id
from services.api_service.db.session import get_sync_session
from services.rag_service.services.chunking import get_chunks_fixed_size
from services.rag_service.services.embedding import embedding_service
from services.api_service.db.models import FileChunk



def process_file_event(event):
    archive_id = event["archive_id"]

    with get_sync_session() as session:
        files = get_files_by_archive_id(archive_id, session)

        for file in files:
            content = file.content
            chunks = get_chunks_fixed_size(content)
            embeddings = embedding_service.embed_texts(chunks)

            for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
                session.add(FileChunk(
                    file_id=file.id,
                    chunk_index=i,
                    text=chunk,
                    vector=vector
                ))

        session.commit()
        session.close()