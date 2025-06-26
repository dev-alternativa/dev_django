class OmieMappingError(Exception):
    """Custom exception for Omie mapping errors."""
    def __init__(self, entity_name, detail):
        self.entity_name = entity_name
        self.detail = detail
        super().__init__(f'{entity_name}: {detail}')