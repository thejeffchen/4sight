"""Claude tool definitions for spreadsheet cell operations."""

CELL_TOOLS = [
    {
        "name": "read_cell",
        "description": "Read the value and formula of a single cell.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sheet": {"type": "string", "description": "Sheet name"},
                "cell_ref": {"type": "string", "description": "Cell reference, e.g. 'B14'"},
            },
            "required": ["sheet", "cell_ref"],
        },
    },
    {
        "name": "read_range",
        "description": "Read a range of cells. Returns a 2D array of values.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sheet": {"type": "string", "description": "Sheet name"},
                "range_ref": {"type": "string", "description": "Range reference, e.g. 'A1:D10'"},
            },
            "required": ["sheet", "range_ref"],
        },
    },
    {
        "name": "write_cell",
        "description": "Write a value to a single cell. The change will be tracked and the user can accept or reject it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sheet": {"type": "string", "description": "Sheet name"},
                "cell_ref": {"type": "string", "description": "Cell reference, e.g. 'B14'"},
                "value": {"description": "Value to write (string, number, or boolean)"},
            },
            "required": ["sheet", "cell_ref", "value"],
        },
    },
    {
        "name": "set_formula",
        "description": "Set a formula in a cell. Must start with '='. The change will be tracked and the user can accept or reject it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sheet": {"type": "string", "description": "Sheet name"},
                "cell_ref": {"type": "string", "description": "Cell reference, e.g. 'B14'"},
                "formula": {"type": "string", "description": "Formula starting with '=', e.g. '=SUM(B2:B9)'"},
            },
            "required": ["sheet", "cell_ref", "formula"],
        },
    },
    {
        "name": "write_range",
        "description": "Write a 2D array of values starting at a cell. Each inner array is a row. All changes are tracked.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sheet": {"type": "string", "description": "Sheet name"},
                "start_cell": {"type": "string", "description": "Top-left cell, e.g. 'A1'"},
                "values": {
                    "type": "array",
                    "items": {"type": "array", "items": {}},
                    "description": "2D array of values, e.g. [[1,2],[3,4]]",
                },
            },
            "required": ["sheet", "start_cell", "values"],
        },
    },
    {
        "name": "get_workbook_structure",
        "description": "Get the structure of the current workbook: sheet names, dimensions, and named ranges.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]
