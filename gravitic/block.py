class Block:
    def __init__(self, specification, pipeline):
        """
        Initialise a production block.
        
        A production block should be a minimal computable unit for 
        part of an analysis.
        """
        self.specification = specification
        self.name = specification['name']
        self.ready = False

    def package(self):
        pass

        
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
