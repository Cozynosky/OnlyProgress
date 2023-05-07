import matplotlib.pyplot as plt
import tensorflow as tf
import pickle

from keras import callbacks
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

PARENT = "D:/Projects/Magisterka/OnlyProgress/"
INPUT_PATH = PARENT + "static/data/downloaded/cropped_faces/"

batch_size = 32
img_height = 180
img_width = 180

def prepare_data():
    train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
    INPUT_PATH,
    validation_split=0.2,
    subset="both",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)
    
    return train_ds, val_ds

def visualise_data(train_ds):
    class_names = train_ds.class_names
    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")
    plt.show()
    
data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)

if __name__ == "__main__":
    train_ds, val_ds = prepare_data()
    #visualise_data(train_ds)
    class_names = train_ds.class_names
    pickle.dump(class_names, open('static/data/bmi_classes.pkl','wb'))
    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    normalization_layer = layers.Rescaling(1./255)
    
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))
    
    num_classes = len(class_names)

    model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
    ])
    
    earlystopping = callbacks.EarlyStopping(monitor="val_loss",
                                        mode="min", patience=3,
                                        restore_best_weights=True)
    
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    
    epochs=50
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks=[earlystopping]
    )
    
    n_epchos = len(history.history["loss"])
    
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    model.save(f"static/data/bmi_models/bmi_model_{n_epchos}e_{round(val_acc[-1] * 10)}")

    epochs_range = range(n_epchos)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()
    
