import bpy

# 기존 객체를 모두 삭제
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# 집 모델링 함수
def create_house():
    # 기초 부분
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))  # 기초
    base = bpy.context.object
    base.name = "House_Base"
    base.data.materials.append(create_material("Gray", (0.5, 0.5, 0.5, 1)))
    
    # 지붕 부분 (집 몸체 위에 위치하도록 조정)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=3, depth=1, location=(0, 0, 2.5))  # 지붕 위치 조정
    roof = bpy.context.object
    roof.name = "House_Roof"
    roof.data.materials.append(create_material("Red", (1, 0, 0, 1)))

    # 문 생성
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, -1.01, 0.5))  # 문
    door = bpy.context.object
    door.name = "House_Door"
    door.data.materials.append(create_material("Brown", (0.5, 0.25, 0.1, 1)))

    # 창문 생성
    for x in [-0.75, 0.75]:
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(x, -1.01, 1))  # 창문
        window = bpy.context.object
        window.name = f"House_Window_{x}"
        window.data.materials.append(create_material("Blue", (0.1, 0.1, 0.5, 0.5)))

# 재질 생성 함수
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = color
    return mat

# BOM 추출 함수
def generate_bom():
    bom = {}
    objects = bpy.data.objects

    for obj in objects:
        if obj.type == 'MESH':
            if obj.name not in bom:
                bom[obj.name] = {"Count": 1}
            else:
                bom[obj.name]["Count"] += 1

    # BOM 내용을 텍스트 파일로 저장
    with open("D:\\MyPython\\gpt-chatbot\\blender_bom.txt", "w") as f:  # 파일 경로는 운영 체제에 맞게 조정 가능
        f.write("BOM (Bill of Materials):\n")
        for name, props in bom.items():
            line = f"{name}: {props['Count']}\n"
            f.write(line)

# 집 생성 및 BOM 출력
create_house()
generate_bom()
print("BOM이 /tmp/bom.txt 파일에 저장되었습니다.")

