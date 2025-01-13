import os
import uuid

def dynamic_filename_for_manager_profile(instance, filename):
    """
    Generates a dynamic file name for manager profiles.
    :param instance: The instance of the model.
    :param filename: The original filename.
    :return: A dynamic file path including DIR_NAME and manager ID.

    """

    # Define directory name for manager profile images
    DIR_NAME = instance.DIR_NAME
    manager_id = str(instance.manager.dl91_id)
    ext = os.path.splitext(filename)[1]  # Extract file extension
    new_filename = f"{manager_id}{ext}"  # Create file name using manager ID
    return os.path.join(DIR_NAME, new_filename)