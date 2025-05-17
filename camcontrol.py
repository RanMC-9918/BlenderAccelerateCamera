import bpy

class Work():
    start = 0
    force = [0, 0, 0]
    duration = 0
    
    def __init__(self, start, force, duration=1):
        self.start = start
        self.force = force
        self.duration = duration
        
class MyProperties(bpy.types.PropertyGroup):
    damping: bpy.props.FloatProperty(name="Dampening", default=0.1)
    affect: bpy.props.FloatProperty(name="Affect", default=0.1)

class CamOperator(bpy.types.Operator):
    bl_idname = "object.cam_ender"
    bl_label = "Render To Selected"
    works = []
    worksR = []
    vel = [0, 0, 0]
    velR = [0, 0, 0]
    damp = 0.1
    dampR = 0.1
    
    def key(self, cam, fr):
        cam.keyframe_insert(data_path="location", frame=fr)
        cam.keyframe_insert(data_path="rotation_euler", frame=fr)
    
    def execute(self, context):
        damp = context.scene.MyProperties.damping
        affect = context.scene.MyProperties.affect
        cam = context.object
        self.key(cam, 0)
        for i in range(1, 200):
            for work in self.works:
                if(work.start <= i and i < work.start + work.duration):
                    self.vel[0] += work.force[0] * affect
                    self.vel[1] += work.force[1] * affect
                    self.vel[2] += work.force[2] * affect
            for work in self.worksR:
                if(work.start <= i and i < work.start + work.duration):
                    self.velR[0] += work.force[0] * affect
                    self.velR[1] += work.force[1] * affect
                    self.velR[2] += work.force[2] * affect
                    
            self.vel[0] -= self.damp * self.vel[0]
            self.vel[1] -= self.damp * self.vel[1]
            self.vel[2] -= self.damp * self.vel[2]
            
            self.velR[0] -= self.dampR * self.velR[0]
            self.velR[1] -= self.dampR * self.velR[1]
            self.velR[2] -= self.dampR * self.velR[2]
                    
            cam.location.x += self.vel[0]
            cam.location.y += self.vel[1]
            cam.location.z += self.vel[2]
            cam.rotation_euler.x += self.velR[0]
            cam.rotation_euler.y += self.velR[1]
            cam.rotation_euler.z += self.velR[2]
            
            self.key(cam, i)
        
        context.scene.frame_set(0)
        return {"FINISHED"}
            
        
 
class CameraP(bpy.types.Panel):
     bl_label = "CamControl"
     bl_idname = "CC"
     bl_space_type = "VIEW_3D"
     bl_region_type = "UI"
     bl_category = "CamControl"
     
     def draw(self, context):
         layout = self.layout
         
         row = layout.row()
         row.label(text = "Console")
         
         layout.prop(context.scene.MyProperties, "damping")
         layout.prop(context.scene.MyProperties, "affect")
         
         layout.operator("object.get_control_data", text="Get Data")
         
         render = layout.operator("object.cam_ender", text="Render Frames")
         
bpy.data.objects.get("control")

class Control(bpy.types.Operator):
    bl_idname = "object.get_control_data"
    bl_label = "Render To Selected"
    
    def execute(self, context):
        control = bpy.data.objects["CamControl"]
        CamOperator.works = []
        CamOperator.workR = []
        
        for fcurve in control.animation_data.action.fcurves:
            keyframes = fcurve.keyframe_points
            if "location" in fcurve.data_path:
                axis_index = fcurve.array_index
                for i in range(int(len(keyframes)/2)):
                    f = [0, 0, 0]
                    f[axis_index] = keyframes[i].co[1]
                    CamOperator.works.append(Work(keyframes[i].co[0], f, keyframes[i+1].co[0]-keyframes[i].co[0]))
                    
                    print(keyframes[i].co[0])
                    print(f)
                    print(keyframes[i+1].co[0]-keyframes[i].co[0])
            elif "rotation_euler" in fcurve.data_path:
                axis_index = fcurve.array_index
                for i in range(int(len(keyframes)/2)):
                    f = [0, 0, 0]
                    f[axis_index] = keyframes[i].co[1]
                    CamOperator.worksR.append(Work(keyframes[i].co[0], f, keyframes[i+1].co[0]-keyframes[i].co[0]))
                    
        return {"FINISHED"}

bpy.utils.register_class(MyProperties)      
bpy.utils.register_class(CamOperator)
bpy.utils.register_class(Control)
bpy.utils.register_class(CameraP) #Panel
bpy.types.Scene.MyProperties   = bpy.props.PointerProperty(type=MyProperties)

