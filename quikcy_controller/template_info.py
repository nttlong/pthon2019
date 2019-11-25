class TemplateInfo:
    def __init__(self,*args,**kwargs):
        self.app=kwargs["app"]
        self.tenancy = kwargs["tenancy"]
        self.rel_template_file_path=kwargs["rel_file_path"]
        self.abs_template_file_path=kwargs["abs_file_path"]
        self.is_static=kwargs["is_static"]