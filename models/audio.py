from sqlmodel import Field, SQLModel, create_engine

class Audio(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name_artist: str
    name_song: str
    full_title: str
    duration: int 
    channel: str | None
    url: str
    file_path: str | None

if __name__ == "__main__":
    test_audio = [
        Audio(
            id=1, 
            name_artist="Mitski", 
            name_song="Washing machine heart (slowed)", 
            full_title="Mitski - Washing machine heart (slowed)", 
            duration=157, 
            channel="Kawwko",
            url="https://www.youtube.com/watch?v=WrpwegGf75Q",
            file_path='\\audio\Mitski - Washing machine heart (slowed)\Mitski - Washing machine heart (slowed).webm.wav',
        ),
    ]

