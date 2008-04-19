from giscanner.gobjecttreebuilder import GLibEnum, GLibEnumMember, GLibFlags
from giscanner.treebuilder import Enum, Function
from giscanner.xmlwriter import XMLWriter

class GIDLWriter(XMLWriter):
    def __init__(self, namespace, nodes):
        super(GIDLWriter, self).__init__()
        self._write_api(namespace, nodes)

    def _write_api(self, namespace, nodes):
        self.push_tag('api', [('version', '1.0')])
        self._write_namespace(namespace, nodes)
        self.pop_tag()

    def _write_namespace(self, namespace, nodes):
        self.push_tag('namespace', [('name', namespace)])
        for node in nodes:
            self._write_node(node)
        self.pop_tag()

    def _write_node(self, node):
        if isinstance(node, Function):
            self._write_function(node)
        elif isinstance(node, Enum):
            self._write_enum(node)
        else:
            print 'Unhandled node', node

    def _write_function(self, func):
        self.push_tag('function', [('name', func.name)])
        self._write_return_type(func.retval)
        self._write_parameters(func.parameters)
        self.pop_tag()

    def _write_return_type(self, return_):
        if not return_:
            return
        self.write_tag('return-type', [('type', return_.type)])

    def _write_parameters(self, parameters):
        if not parameters:
            return
        self.push_tag('parameters')
        for parameter in parameters:
            self._write_parameter(parameter)
        self.pop_tag()

    def _write_parameter(self, parameter):
        self.write_tag('parameter', [('name', parameter.name),
                                     ('type', parameter.type)])

    def _write_enum(self, enum):
        attrs = [('name', enum.name)]
        tag_name = 'enum'
        if isinstance(enum, GLibEnum):
            attrs.append(('get-type', enum.get_type))
            if isinstance(enum, GLibFlags):
                tag_name = 'flags'

        self.push_tag(tag_name, attrs)
        for member in enum.members:
            self._write_member(member)
        self.pop_tag()

    def _write_member(self, member):
        attrs = [('name', member.name),
                 ('value', str(member.value))]
        if isinstance(member, GLibEnumMember):
            attrs.append(('nick', member.nick))
        self.write_tag('member', attrs)
