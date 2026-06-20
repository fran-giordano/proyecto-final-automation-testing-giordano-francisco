from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    _TITLE = (By.CLASS_NAME, "title")
    _PRODUCTS = (By.CLASS_NAME, "inventory_item")
    _ADD_BUTTONS_ = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
    def obtener_titulo(self):
        """Obtiene el título de la página de inventario."""
        return self.wait.until(EC.visibility_of_element_located(self._TITLE))
        
    def obtener_productos(self):
        return self.driver.find_elements(*self._PRODUCTS)
        
    def agregar_al_carrito(self):
        primer_boton = self.driver.find_elements(*self._ADD_BUTTONS_)[0]
        primer_boton.click()
        return self
        
    def obtener_contador_carrito(self) -> int:
        """Obtiene la cantidad de productos en el carrito."""
        try: 
            badge = self.driver.find_element(*self._CART_BADGE)
            return int(badge.text)
        except:
            return 0
            
    def ir_al_carrito(self):
        self.driver.find_element(*self._CART_LINK).click()
        # Importación para evitar dependencias ciruclares
        from pages.cart_page import CartPage
        return CartPage(self.driver)
    
    def add_to_cart(self, nombre_producto: str):
        """Agrega un producto al carrito por su nombre."""
        productos = self.obtener_productos()
        for producto in productos:
            nombre = producto.find_element(By.CLASS_NAME, "inventory_item_name").text
            if nombre == nombre_producto:
                boton = producto.find_element(By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
                boton.click()
                return self
        raise ValueError(f"Producto '{nombre_producto}' no encontrado en el catálogo.")
    
    def cart_count(self) -> int:
        return self.obtener_contador_carrito()

    def cerrar_sesion(self):
        self.driver.find_element(*self._MENU_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(self._LOGOUT_LINK)).click()
        # Importación para evitar dependencias ciruclares
        from pages.login_page import LoginPage
        return LoginPage(self.driver)
    
    
    
            