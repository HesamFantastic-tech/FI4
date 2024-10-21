from swagger_ui import api_doc
import main


api_doc(main, config_path='./config/test.yaml', url_prefix='/api/doc', title='API doc')