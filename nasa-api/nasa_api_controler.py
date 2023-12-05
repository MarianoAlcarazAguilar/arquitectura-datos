from owslib.wms import WebMapService
from IPython.display import Image
import os

class NasaControler:
    '''
    Esta clase sirve para sacar imágenes satelitales usando la api de la nasa.
    Tan solo es necesario darle una fecha y te regresa la imagen de ese día.
    '''
    def __init__(self, images_folder:str='.'):
        self.wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')
        self.img = None
        self.date = None
        self.images_folder = self.__validate_images_folder(images_folder=images_folder)

    def __validate_images_folder(self, images_folder:str):
        '''
        Esta función se asegura de que el folder para las imágenes exista.
        En caso contrario, lo crea.
        '''
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        return images_folder
        
    def load_image(self, date:str, save:bool=False):
        '''
        Esta función carga la imagen y la guarda en el objeto. No regresa nada.
        Formato de la fecha: 'yyyy-mm-dd'
        
        Si save es True, se guarda la imagen en la ubicación default. Para más control
        sobre el guardado de la imagen, usar la función save_image()
        '''
        img = self.wms.getmap(
            layers=['MODIS_Terra_CorrectedReflectance_TrueColor'],  # Layers
            srs='epsg:4326',  # Map projection
            bbox=(-180,-90,180,90),  # Bounds
            size=(1200, 600),  # Image size
            time=date,  # Time of data
            format='image/png',  # Image format
            transparent=True  # Nodata transparency
        ) 
        self.img = img
        self.date = date
        if save:
            self.save_image()
    
    def save_image(self, location:str=None):
        '''
        Esta función guarda la imagen en la ubicación especificada.
        Si no se da ninguna ubicación (None) se guarda en la carpeta especificada
        en images_folder con el nombre de la fecha que se buscó.
        '''
        assert self.img is not None, "No image has been loaded yet"
        if location is None:
            location = f'{self.images_folder}/{self.date}.png'
        with open(location, 'wb') as f:
            f.write(self.img.read())

    def display_image(self):
        assert self.img is not None, "No image has been loaded yet"
        return Image(self.img.read())
    

if __name__ == '__main__':
    image_controler = NasaControler()
    image_controler.load_image('2023-10-11')
    image_controler.save_image('./image_prueba.png')