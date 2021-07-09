import os

class Block:
    def __init__(self, specification, pipeline):
        """
        Initialise a production block.
        
        A production block should be a minimal computable unit for 
        part of an analysis.
        """
        self.pipeline = pipeline
        self.specification_dict = specification
        self.name = specification['name']
        self.ready = False
        self.input_blocks = self.dependencies
        self.input_data = {}
        for block in self.input_blocks:
            self.input_data.update({filename: data
                                    for filename, data
                                    in pipeline.blocks[block].output_files.items()})
            for datum, location in self.input_data.items():
                self.input_data[datum] = os.path.join(
                    self.pipeline.run_location,
                    location)
        
        if "status" in specification:
            self.status_flag = specification['status']
        else:
            self.status_flag = None

               
    def package(self):
        pass
    
    @property
    def specification(self):
        """
        Return the current Block specification.
        """
        specification = self.specification_dict
        specification['status'] = self.status
        specification['outputs'] = self.output_files
        return specification

    @property
    def status(self):
        return self.status_flag

    @property
    def finished(self):
        if self.status in {"finished", "uploaded"}:
            return True
        else:
            return False
    
    @status.setter
    def status(self, flag):
        """
        Set the status of this block.
        """
        self.status_flag = flag

    @property
    def dependencies(self):
        if "needs" in self.specification_dict:
            if isinstance(self.specification_dict['needs'], list):
                return self.specification_dict['needs']
            else:
                return [self.specification_dict['needs']]
        else:
            return []

class BlockMap:
    def __init__(self):
        self.known_blocks = {}
        # Add the manual block
        self.known_blocks['manual'] = Block
    def register_block(self,name, block):
        self.known_blocks[name] = block
    def __getitem__(self, item):
        return self.known_blocks[item]
blockmap = BlockMap()

