from html.parser import HTMLParser
from djazz.formatters import FormatterBase
from django.utils.html import escape as html_escape

class FilteredParser(HTMLParser):
    
    def __init__(self, method="allow", tags=[]):
        super(FilteredParser, self).__init__()
        self.method = method
        self.tags = [tag.lower() for tag in tags]
    
    def scan_tag(self, tag, attrs=None):
        self.close_last_tag()
        
        if self.method == "allow" and not tag in self.tags:
            self.cursors.append([tag, attrs, self.getpos()])
            self.last_open = [self.getpos(), "tag"]
        elif self.method == "deny" and tag in self.tags:
            self.cursors.append([tag, attrs, self.getpos()])
            self.last_open = [self.getpos(), "tag"]
        else:
            self.last_open = [self.getpos(), "other"]
    
    def scan_other(self):
        self.close_last_tag()
        self.last_open = [self.getpos(), None]
    
    def close_last_tag(self):
        if self.last_open[1] == "tag":
            line, col = self.getpos()
            self.cursors[-1].append((line, col - 1))
    
    def handle_starttag(self, tag, attrs):
        self.scan_tag(tag, attrs)
    
    def handle_endtag(self, tag):
        self.scan_tag(tag, None)
    
    def handle_startendtag(self, tag, attrs):
        self.scan_tag(tag, attrs)
    
    def handle_data(self, data):
        self.scan_other()
    def handle_charref(self, name):
        self.scan_other()
    def handle_comment(self, data):
        self.scan_other()
    def handle_decl(self, decl):
        self.scan_other()
    def handle_pi(self, data):
        self.scan_other()
    def unknown_decl(self, decl):
        self.scan_other()
    
    def feed(self, data):
        self.cursors = []
        self.last_open = [0, None]
        super(FilteredParser, self).feed(data)
        self.close_last_tag()
        
        splitted = data.split("\n")
        filtered = ""
        last_pos = (1, 0)
        end_pos = (len(splitted), len(splitted[-1]))
        
        for cursor in self.cursors:
            # Join safe text
            filtered += self.join_filtered_html(splitted, last_pos, cursor[2])
            
            # Escape unallowed html tags
            filtered += self.join_escaped_html(splitted, cursor[2], cursor[3])
            
            last_pos = cursor[3]
        filtered += self.join_filtered_html(splitted, last_pos, end_pos)
        return filtered
    
    def join_filtered_html(self, splitted_data, pos_left, pos_right):
        lines = splitted_data[pos_left[0]-1:pos_right[0]]
        if len(lines) == 1:
            return lines[0][pos_left[1]+1:pos_right[1]]
        else:
            lines[0] = lines[0][pos_left[1]+1:]
            lines[-1] = lines[-1][:pos_right[1]]
            return "\n".join(lines)
    
    def join_escaped_html(self, splitted_data, pos_left, pos_right):
        lines = splitted_data[pos_left[0]-1:pos_right[0]]
        if len(lines) == 1:
            return html_escape(lines[0][pos_left[1]:pos_right[1]+1])
        else:
            lines[0] = lines[0][pos_left[1]:]
            lines[-1] = lines[-1][:pos_right[1]+1]
            return html_escape("\n".join(lines))


class Formatter(FormatterBase):
    
    def filter(self, text, method="allow", tags=["h1"], **kwargs):
        parser = FilteredParser(method, tags)
        return parser.feed(text)
    
    def process(self, text):
        return text
