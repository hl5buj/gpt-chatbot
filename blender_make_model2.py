import bpy

# 기존 객체를 모두 삭제
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# 집 모델링 함수
def create_house():
    wall_height = 2  # 벽 높이
    door_height = wall_height * 0.7  # 문 높이 (집 본체 높이의 70%)
    door_width = wall_height * 0.5  # 문 폭 (집 높이의 50%)
    window_height = 0.5  # 창문 높이
    window_width = 0.75  # 창문 폭
    base_size = 2  # 집 본체 크기

    # 기초 부분
    bpy.ops.mesh.primitive_cube_add(size=base_size, location=(0, 0, wall_height / 2))  # 기초
    base = bpy.context.object
    base.name = "House_Base"
    base.data.materials.append(create_material("Gray", (0.5, 0.5, 0.5, 1)))

    # 지붕 부분 (집 몸체 위에 맞춤)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=base_size * 1.5, depth=1, location=(0, 0, wall_height + 0.5))  # 지붕 높이 조정
    roof = bpy.context.object
    roof.name = "House_Roof"
    roof.data.materials.append(create_material("Red", (1, 0, 0, 1)))

    # 문 생성 (바닥에 닿도록 하고 회전 설정)
    bpy.ops.mesh.primitive_cube_add(size=door_width, location=(0, -1.01, door_height / 2))  # 문
    door = bpy.context.object
    door.name = "House_Door"
    door.scale[0] = 0.1  # 문 두께
    door.scale[1] = door_width / 2  # 문 폭
    door.scale[2] = door_height     # 문 높이
    door.rotation_euler[2] = 1.5708  # 90도 회전 (라디안)
    door.data.materials.append(create_material("Brown", (0.5, 0.25, 0.1, 1)))

    # 앞쪽 창문 생성
    for x in [-0.75, 0.75]:
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(x, -1.01, wall_height * 0.5))  # 창문
        window = bpy.context.object
        window.name = f"House_Window_Front_{x}"
        window.scale[0] = window_width  # 창문 폭
        window.scale[1] = 0.05  # 얇은 두께
        window.scale[2] = window_height * 3  # 창문 높이
        window.data.materials.append(create_material("Blue", (0.1, 0.1, 0.5, 0.5)))

    # 우측 창문 생성 (50% 크기)
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1.01, 0, wall_height * 0.5))  # 우측 창문
    side_window_right = bpy.context.object
    side_window_right.name = "House_Window_Side_Right"
    side_window_right.scale[0] = base_size * 1.5  # 창문 폭 (50% 크기)
    side_window_right.scale[1] = 0.05  # 얇은 두께
    side_window_right.scale[2] = window_height * 3   # 창문 높이
    side_window_right.rotation_euler[2] = 1.5708  # 90도 회전 (라디안)
    side_window_right.data.materials.append(create_material("Blue", (0.1, 0.1, 0.5, 0.5)))

    # 좌측 창문 생성 (50% 크기)
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(-1.01, 0, wall_height * 0.5))  # 좌측 창문
    side_window_left = bpy.context.object
    side_window_left.name = "House_Window_Side_Left"
    side_window_left.scale[0] = base_size * 1.5  # 창문 폭 (50% 크기)
    side_window_left.scale[1] = 0.05  # 얇은 두께
    side_window_left.scale[2] = window_height * 3  # 창문 높이
    side_window_left.rotation_euler[2] = 1.5708  # 90도 회전 (라디안)
    side_window_left.data.materials.append(create_material("Blue", (0.1, 0.1, 0.5, 0.5)))

    # 뒤쪽 창문 생성 (50% 크기)
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 1.01, wall_height * 0.5))  # 뒤쪽 창문
    back_window = bpy.context.object
    back_window.name = "House_Window_Back"
    back_window.scale[0] = base_size * 1.5  # 창문 폭 (50% 크기)
    back_window.scale[1] = 0.05  # 얇은 두께
    back_window.scale[2] = window_height * 3  # 창문 높이
    back_window.data.materials.append(create_material("Blue", (0.1, 0.1, 0.5, 0.5)))

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
    with open("D:\\MyPython\\gpt-chatbot\\house_bom.txt", "w") as f:  # 파일 경로는 운영 체제에 맞게 조정 가능
        f.write("BOM (Bill of Materials):\n")
        for name, props in bom.items():
            line = f"{name}: {props['Count']}\n"
            f.write(line)

# 집 생성 및 BOM 출력
create_house()
generate_bom()
print("BOM이 house_bom.txt 파일에 저장되었습니다.")



