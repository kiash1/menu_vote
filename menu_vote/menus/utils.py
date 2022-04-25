def menu_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>-<restaurant_name>/<filename>
    return "{0}-{1}/{2}".format(instance.restaurant.id, instance.restaurant.name, filename)
