class Validations:

    @staticmethod
    def validate_enum(value, enum) -> bool:
        try:
            return any(value == item.value for item in enum)
        except Exception as e:
            print(f"Error in validate_enum: {str(e)}")
            raise e
