class Plant:
    def __init__(self,regional_bias,random=False,weighted=False):
        #data is probably going to be assigned by inheritance from a game object
        self._data = {"id":"UUID",
        "date_created":"date_timestamp",
        "version":"sample_version",
        "size_string":"descriptive_size_tag",
        "size_val":0,
        "price":0,
        "price_string":"descriptive_price_string"}
        self._plant_bias_obj = self._generate_bias_obj()
        self.plant=None
        self.plant_name = None
        self.regions = {1:'Centriss',2:'Tentacular',3:'Mormiria',4:'Tirelessnight',5:'Reyawinn',0:'Xilewood'}
        self.locaitons= {1:}
        self.regional_bias = (regional_bias,self.get_regional_bias_int(regional_bias))
        self.all_plants_in_region=self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe'].iloc[1,:][1:].tolist()
        self._plant_id = "create a unique ID based upon a generated NAME for the plant so I can identify when stuff gets made"
        self.potence = -1
    def get_regional_bias_int(self,r):
        return [i for i in self.regions if self.regions[i]==r][0]
    def _sanitize_bias_keystring(self,filepath):
        return re.search(r'.*\_',filepath).group(0)[7:-1].capitalize()
    def _generate_bias_obj(self):
        obj={}
        bias_dir=r'./bias/'
        try:
            i=0
            for file in os.listdir(bias_dir):
                filepath = os.path.join(bias_dir,file)
                obj[self._sanitize_bias_keystring(filepath)] = {'_name':self._sanitize_bias_keystring(filepath),'id':i,f'_filestring':filepath,'_dataframe':pd.read_csv(filepath, encoding='utf-8',delimiter='|'),'base':}
                i+=1
        except Exception as e:
            raise ValueError(f'Could not load the biases files - Error:{e}')
        return obj

class Plant:
    def __init__(self, regional_bias, random=False, weighted=False):
        # Assign default data
        self._data = {
            "id": "UUID",
            "date_created": "date_timestamp",
            "version": "sample_version",
            "size_string": "descriptive_size_tag",
            "size_val": 0,
            "price": 0,
            "price_string": "descriptive_price_string"
        }
        # Generate bias object
        self._plant_bias_obj = self._generate_bias_obj()

        # Initialize variables
        self.plant = None
        self.plant_name = None

        # Define regions
        self.regions = {
            1: "Centriss",
            2: "Tentacular",
            3: "Mormiria",
            4: "Tirelessnight",
            5: "Reyawinn",
            0: "Xilewood"
        }

        # Define locations
        self.locations = {
            1: ...
        }

        # Store regional bias
        self.regional_bias = (regional_bias, self.get_regional_bias_int(regional_bias))

        # Store plant names in region
        self.all_plantnames_in_region = self._plant_bias_obj[self.regions[self.regional_bias[1]]]['_dataframe'].iloc[1, :][1:].t



        ##########ACTUAL#############

