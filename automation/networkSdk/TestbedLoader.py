import os
import re
import sys
import yaml
import logging
import collections
from networkSdk.testbed import Testbed, VirtualTestbed
from networkSdk.link import Link
from networkSdk.interface import Interface
from networkSdk.device import Device

logger = logging.getLogger(__name__)

class TestbedLoader(object):
#    def __init__(self):
#        ''' load and store the schema file internally '''
#        print ("TesbedLoader Initiated")

    def load(self, loadable):
        '''Load Function

        API to load a 'loadable' into corresponding physicalTestbed objects. This API
        is mainly responsible for creating physicalTestbed objects from the given
        loadable configuration, and it uses load_configuration API to do the
        actual loading of the 'loadable' into dict format that it needs
        internally.

        Arguments
        ---------
            loadable (obj): passed through to load_configuration API.

        Returns
        -------
            Testbed object, along with all the device/Intferface/Link objects
            instanciated and the relationship fully built and stored into the
            physicalTestbed object.
        '''

        # load configuration

        config = self.load_configuration(loadable)
        print("\n\nTestbedLoader : \n config = ",config,"\n\n")

        # # create Testbed object from physicalTestbed configs
        testbed = Testbed(**config['testbed'])
        print("\n\ntestbed = ",dir(testbed))

        #
        # # set testbed_file field to physicalTestbed object
        if isinstance(loadable, str) and os.path.isfile(loadable):
            testbed.testbed_file = loadable

        # # create device objects from device section, add to physicalTestbed
        for name, device in config['devices'].items():
            print("\n\n name = ",name,\
                  "\n device = ",device)
            testbed.add_device(Device(name = name,**device))

        #
        # # parse topology block
        # #   1. find the link fields and replace the with actual link objects
        # #   2. create interfaces and add them to links
        # #   3. add interfaces to each device object.
        #
        # # track all the unique links in this topology
        links = {}
        #
        # # process if there's extended link information section
        # if 'links' in config['topology']:
        #     # make sure to pop the links section so that it doesn't get
        #     # treated as a device
        #     for name, linkinfo in config['topology'].pop('links').items():
        #         links[name] = Link(name = name, **linkinfo)
        #
        # # process devices in topology section
        for device in config['topology']:
            #if device not in physicalTestbed.devices:
                #raise MissingDeviceError(device)

            interfaces = config['topology'][device]['interfaces']
            print("\n\ninterfaces = ", interfaces)

            for name, intf in interfaces.items():
                print("name = ",name,"intf = ", intf)
                if 'link' in intf:
                    # interface contains a link
                    linkname = intf['link']
                    if linkname not in links:
                        links[linkname] = Link(name = linkname)
                    intf = intf.copy()
                    intf.update(link = links[linkname])
                testbed.devices[device].add_intf(Interface(name = name, **intf))            
        
        print("Final testbed = ",testbed.__dict__)
        return testbed

    def load_configuration(self, loadable):
        '''Load Configuration

        API to load a 'loadable' into a dictionary format, set defaults, and
        validates it against the YAML schema.

        Loadables
        ---------
            - dictionary respecting the yaml schema format
            - full path/name of the yaml physicalTestbed file
            - any yaml python stream readable by yaml.safe_load api

        Arguments
        ---------
            loadable (obj): a loadable (as above)

        Returns
        -------
            dict() format particular to the schema definition.
        '''
        if loadable is None:
            # special condition, loading nothing should yield the defaults
            config = {}
        elif isinstance(loadable, str) and os.path.isfile(loadable):
            # user provided a yaml file
            config = self.load_yaml(loadable)
            print(yaml.dump(config, default_flow_style=False, default_style='' ))

        elif isinstance(loadable, collections.MutableMapping):
            # user provided a dict config
            config = loadable
        else:
            # don't know what the user provided
            # last measure, try to tackle it as a loadable stream
            try:
                config = yaml.safe_load(loadable)
            except Exception as e:
                raise e

        # set defaults
        # converts  None and '' to {}s, as topology always expects dicts.
        config['physicalTestbed'] = config.get('physicalTestbed', {}) or {}
        config['devices'] = config.get('devices', {}) or {}
        config['topology'] = config.get('topology', {}) or {}

        # try and get the physicalTestbed name
        try:
            name = config['physicalTestbed']['name']
        except:
            if isinstance(loadable, str) and os.path.isfile(loadable):
                filename = os.path.basename(loadable)
                if filename.startswith('CONFIG.'):
                    # name in the format of CONFIG.<tbname> (or other)
                    # assume last word is tb name
                    name = filename.split('.')[1]
                else:
                    # name in the format of <tbname>.yaml (or other)
                    # assume first word is physicalTestbed name
                    name = filename.split('.')[0]
            else:
                # no name provided
                name = ''
        finally:
            config['physicalTestbed']['name'] = name

        # now verify against the schema
        #config = self.schema.validate(config)

        # now process the markups
        #config = self.processMarkup(config)

        return config


    def load_yaml(self, yaml_file):
        '''Loading YAML config file

        API to load a YAML based config file and return its content in dict.

        Arguments
        ---------
            yaml_file (str): path to file including the full file name

        Returns
        -------
            dict of information contained in config file
        '''

        logger.debug('loading yaml file %s' % yaml_file)

        try:
            with open(yaml_file, 'r') as testbed_file:
                data = yaml.safe_load(testbed_file)
        except Exception as e:
            raise e

        # check there is inforamtion in the testbed file
        if not data:
            logger.warning("The yaml file '%s' is empty." % yaml_file)

        return data

    def chainAttr(self, attr, obj):
        '''ChainAttr

        Helper function, converts attribute lists into chained attribute access.

        Example
        -------
            >>> chainAttr(['a','b','c'], obj)
            # is equivalent to
            >>> obj.a.b.c

        Arguments
        ---------
            attr (list): string list of attribute names to chain access
            obj (obj): any object to be chain accessed

        Returns
        -------
            the final object attribute
        '''

        if not attr:
            return obj
        else:
            return self.chainAttr(attr, obj[attr.pop(0)])



