from django.db import models 
from django.core.exceptions import ValidationError


class Category(models.Model): 
    name = models.CharField(max_length=120)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    @staticmethod
    def get_all_categories(): 
        return Category.objects.all() 

    def __str__(self): 
        return ( str(self.parent) + "---" if self.parent else "" ) + self.name 

    def get_descendants(category):
        descendants = []
        children = category.children.all()
        for child in children:
            descendants.append(child)
            descendants.extend(get_descendants(child))
        return descendants

    def get_parent(self):
        return self.parent

    def clean(self):
        if self.parent == self:
            raise ValidationError("A category cannot be its own parent")
    # def get_objects_by_referenced_id_code(id_code_value):
    #     referenced_objects = ReferencedModel.objects.filter(id_code=id_code_value)
    #     objects_with_referenced = MyModel.objects.filter(referenced__in=referenced_objects)
    #     return objects_with_referenced
