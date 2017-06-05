from .attrdict import AttrDict

class DeviceDict(AttrDict):
    def __init__(self, **kwargs):
        super(DeviceDict, self).__init__(**kwargs)
        self.__dict__ = self

    def __getitem__(self, key):
        for name, value in self.items():
#            print("name = ", name,", value = ",value)
            if key in name or key == value.alias :
                return value
        #return dict.__getitem__(self, key)

if __name__ == '__main__':

    input = AttrDict(name="2", alias='hello')
    #input.update(AttrDict(name=5, alias='5japs'))
    print ("input = ",input.name)
    name=input.name
    print ("name = ",name)
    output = DeviceDict(**input)
    input.update(AttrDict(name="5", alias='hello2'))
    print ("input = ",input)
    print("\n\noutput = ",output)
    ss={name: "hello","age":12}
    print(ss[name])
    print(ss["age"])    
#    print (output["5"])
