import json


class SerializableUtility:
    @staticmethod
    def serialize_json(data: dict) -> str:
        try:
            return json.dumps(data, separators=(",", ":"), default=str)  # Convierte enum a str automáticamente
        except Exception as e:
            print(f"Error in serialize_json: {str(e)}")
            raise e

    @staticmethod
    def deserialize_json(data: str) -> dict:
        return json.loads(data)
