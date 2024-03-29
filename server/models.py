from sqlalchemy import Column, Integer, String

from server.database import database


class Score(database.Model):
    id = Column(Integer, primary_key=True)
    distance = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    name = Column(String(6), nullable=False)

    @staticmethod
    def as_json_list(count=-1, name=None, id=False):
        """

        :param count: specify how many scores you want it to return
        :param name: specify a name of a player you want the scores of
        :param id: specify if the db id should be included
        :return: list of scores
        """
        scores = Score.query.many()
        if name:
            scores = [score for score in scores if score.name.lower().strip() == name.lower().strip()]
        scores.sort(key=lambda x: x.points, reverse=True)
        scores = [score.to_json(id=id) for score in scores]
        # max stored runs
        while len(scores) > 50000:
            score = scores.pop()
            with database:
                Score.query.delete_by(id=score["id"])
        return scores[0:count] if count > 0 else scores

    @staticmethod
    def from_json(json):
        try:
            # return if name is too long
            if len(json["name"]) > 6:
                return None

            return Score(
                distance=int(json["distance"]),
                points=int(json["points"]),
                name=json["name"].strip(),
            )
        # bad practice, DONT TRY @ HOME!!
        except:
            return None
