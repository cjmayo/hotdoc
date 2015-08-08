class Link (object):
    def get_link (self):
        raise NotImplementedError

class ExternalLink (Link):
    def __init__ (self, symbol, local_prefix, remote_prefix, filename, title):
        self.symbol = symbol
        self.local_prefix = local_prefix
        self.remote_prefix = remote_prefix
        self.filename = filename
        self.title = title

    def get_link (self):
        return "%s/%s" % (self.remote_prefix, self.filename)


class LocalLink (Link):
    def __init__(self, id_, pagename, title):
        self.id_ = id_
        self.pagename = pagename
        self.title = title

    def get_link (self):
        if (self.id_):
            return "%s#%s" % (self.pagename, self.id_)
        else:
            return self.pagename


class LinkResolver(object):
    def __init__(self):
        self.__external_links = {}
        self.__local_links = {}

    def get_named_link (self, name):
        link = None
        try:
            link = self.__local_links[name]
        except KeyError:
            try:
                link = self.__external_links[name]
            except KeyError:
                pass
        return link

    def add_local_link (self, link):
        self.__local_links[link.title] = link

    def add_external_link (self, link):
        self.__external_links[link.title] = link


link_resolver = LinkResolver()