from sqlalchemy import Column, Integer, String

from server.database import database


class Score(database.Model):
    id = Column(Integer, primary_key=True)
    distance = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    name = Column(String(6), nullable=False)

    @staticmethod
    def as_json_list(count=-1, name=None):
        scores = Score.query.many() if name is None else Score.query.many(name=name)
        scores.sort(key=lambda x: x.points, reverse=True)
        scores = [score.to_json() for score in scores]
        return scores[0:count] if count > 0 else scores

    @staticmethod
    def from_json(json):
        return Score(
            distance=int(json["distance"]),
            points=int(json["points"]),
            name=json["name"],
        )
