from spade.template.parser import TemplateParser
from spade.template.ast import Ast, StructDecl, FieldDecl, ArrayDecl

def validate_field(field, type_, name):
    assert field is not None
    assert type(field) is FieldDecl
    assert field.type == type_
    assert field.name == name

def validate_array(array, size, type_, name):
    assert array is not None
    assert type(array) is ArrayDecl
    assert array.size == size
    assert array.field is not None
    assert array.field.type == type_
    assert array.field.name == name

def validate_header(struct):
    assert struct is not None
    assert struct.name == "header_t"
    assert len(struct.fields) == 4

    # Validate char signature[4] field
    array = struct.fields[0]
    assert array is not None
    assert type(array) is ArrayDecl
    assert array.size == 4
    assert array.field is not None
    assert array.field.type == "char"
    assert array.field.name == "signature"

    validate_array(struct.fields[0], 4, "char", "signature")
    validate_field(struct.fields[1], "int", "field1")
    validate_field(struct.fields[2], "int", "field2")
    validate_field(struct.fields[3], "int", "blob_amt")

def validate_blob(struct):
    assert struct is not None
    assert struct.name == "blob_t"
    assert len(struct.fields) == 1

    # Validate fields
    validate_field(struct.fields[0], "int", "size")

def validate_file(struct):
    assert struct is not None
    assert struct.name == "FILE"
    assert len(struct.fields) == 1

    # Validate fields
    validate_field(struct.fields[0], "header_t", "header")

def test_parser_validtemplate1():
    # Parse template
    parser = TemplateParser()
    assert parser is not None
    ast = parser.parse_file("tests/template/validtemplate1.stf")
    assert ast is not None

    # Do we have all our structs?
    assert ast.structs is not None
    assert len(ast.structs) == 3

    # Make sure all expected structs exist and are good in ast
    expected_structs = ["header_t", "blob_t", "FILE"]
    for struct in ast.structs:
        for s in expected_structs:
            if struct.name == s:
                expected_structs.remove(s)
    assert len(expected_structs) == 0

    # Validate structs
    validate_header(ast.struct("header_t"))
    validate_blob(ast.struct("blob_t"))
    validate_file(ast.struct("FILE"))