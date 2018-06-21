import os
import keras
import redis

BASE_MODEL_PATH = os.path.join("app", "models", "vgg16", "base", "base.h5")
TOPLESS_MODEL_PATH = os.path.join("app", "models", "vgg16", "topless")

# loading base model
if os.path.exists(BASE_MODEL_PATH):
    print "* Starting: Found Base Model."
else:
    print "* Starting: No Base Model Found. Loading..."
    base_model = keras.applications.vgg16.VGG16(include_top=True, 
                                                    weights='imagenet',
                                                    input_shape=(224, 224, 3))
    base_model.save(BASE_MODEL_PATH)
    print "* Starting: Base Model Saved!"
    
# loading topless model
if os.path.exists(TOPLESS_MODEL_PATH):
    print "* Starting: Found Topless Model."
else:
    os.makedirs(TOPLESS_MODEL_PATH)
    print "* Starting: No Topless Model Found. Loading..."
    base_model = keras.applications.vgg16.VGG16(include_top=False, 
                                                    weights='imagenet',
                                                    input_shape=(224, 224, 3))
    base_model.save(os.path.join(TOPLESS_MODEL_PATH, "topless.h5"))
    print "* Starting: Topless Model Saved!"
    
# clean up the died images upon start:
# need to wait a bit for redis container to start up
pool = redis.ConnectionPool(host='redis', port=6379, db=0)
db = redis.Redis(connection_pool=pool)
db.flushall()