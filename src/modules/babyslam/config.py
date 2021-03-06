from xml.dom import minidom
from babyslam import effects
import pygame
import random, os

class XmlConfigBuilder(object):
  def __init__(self):
    self.item_weight = {}
    pass

  def build_config(self, xmlconfig):
    result = Config()
    self.collect_effects(xmlconfig, result)
    return result
 
  def collect_effects(self, xmlconfig, cfg):
    xmldoc = minidom.parse(xmlconfig)
    config_el = xmldoc.firstChild
    global_el = xmldoc.getElementsByTagName('global').item(0)

    split = os.path.split(xmlconfig)[:-1]
    basedir = split[0]
    for p in split[1:]:
      basedir = os.path.join(basedir, p)

    if global_el != None:
      basedir = self.readStringValue(global_el, 'basedir', '/usr/share/babyslam/media') #FIXME: hardcoded path

      escapeclause = self.readStringValue(global_el, 'escapeclause', None)
      if escapeclause != None:
        cfg.escapeclause = escapeclause

    for importdirs_el in xmldoc.getElementsByTagName('importdirs'):
      import_root = importdirs_el.firstChild.data
      if not os.path.exists(os.path.expanduser(import_root)):
        print "%s does not exist, nothing imported"%import_root
      else:
        print "Importing subdirs from %s"%import_root
        import_root=os.path.expanduser(import_root)
        for subdir in os.listdir(import_root):
          subdir = os.path.join(import_root, subdir)
          if not os.path.isdir(subdir):
            print "%s skipped (not a directory)"%subdir
            continue
          subxml = os.path.join(import_root, subdir,'config.xml')
          if not os.path.exists(subxml):
            print "%s does not exist, directory skipped"%subxml
            continue
          self.collect_effects(str(subxml), cfg)

    for set_el in xmldoc.getElementsByTagName('set'):
      for item_el in set_el.getElementsByTagName('item'):
        for effect_el in item_el.getElementsByTagName('effect'):
          type = effect_el.getAttribute('type')
          weight = item_el.getAttribute('weight')
          weight = int(weight) if weight!='' else 1

          #TODO: handle missing images, sounds, ... more graceously
          if type == 'letter':
            cfg.add_effect(weight, self.build_letter_effect(basedir, item_el, effect_el))
          elif type == 'rotate':
            cfg.add_effect(weight, self.build_rotate_effect(basedir, item_el, effect_el))
          elif type == 'flip':
            cfg.add_effect(weight, self.build_flip_effect(basedir, item_el, effect_el))
          elif type == 'race':
            cfg.add_effect(weight, self.build_race_effect(basedir, item_el, effect_el))
          else:
            print "Unknown effect type %s."%type

  def add_item(self, item, weight):
    self.item_weight[item] = weight

  def get_base_data(self, basedir, item_el):
    images = []
    sound = None

    for image_el in item_el.getElementsByTagName('image'):
      images.append(os.path.join(basedir, image_el.firstChild.data))
    for sound_el in item_el.getElementsByTagName('sound'):
      sound = pygame.mixer.Sound(os.path.join(basedir, sound_el.firstChild.data))
    return images, sound

  def build_letter_effect(self, basedir, item_el, effect_el):
    return effects.LetterEffect()

  def build_rotate_effect(self, basedir, item_el, effect_el):
    images, sound = self.get_base_data(basedir, item_el)
    return effects.RotateEffect(images, sound)

  def build_flip_effect(self, basedir, item_el, effect_el):
    images, sound = self.get_base_data(basedir, item_el)
    return effects.FlipEffect(images, sound)

  def build_race_effect(self, basedir, item_el, effect_el):
    images, sound = self.get_base_data(basedir, item_el)
    return effects.RaceEffect(images, sound)

  def readStringValue(self, element, child_name, default):
    child_el = element.getElementsByTagName(child_name).item(0)
    print child_el
    if child_el == None:
      print 'no child named', child_name, '. returning ', default
      return default
    else:
      print 'child named', child_name, 'has value', child_el.firstChild.data
      return child_el.firstChild.data

class Config:
  # effects should be a sorted list of (cumul, item) pairs
  def __init__(self):
    self.effects = []
    self.cumul = 0
    self.escapeclause = 'babydodo'

  def add_effect(self, weight, effect):
    self.cumul += weight
    self.effects.append([self.cumul, effect])

  def get_random_effect(self, char):
    max = self.effects[-1][0]
    r = random.random()*max
    # find the first element whose cumul > r
    return filter(lambda x: x[0]>r, self.effects)[0][1].create_instance(char)
