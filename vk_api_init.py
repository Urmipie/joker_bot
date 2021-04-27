from vk_api import VkApi
from credential import VK_TOKEN


vk_sess = VkApi(token=VK_TOKEN)
VK = vk_sess.get_api()
