import os, sublime, sublime_plugin, webbrowser

API_URL = 'http://jsfiddle.net/api/post/library/pure/'

DESCR = 'Created by SendToJsfiddle Sublime Text Plugin'

class SendToJsfiddleCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    paste_title = self.view.file_name()

    if paste_title is not None:
      paste_title = os.path.basename(paste_title)
    else:
      paste_title = 'Untitled'

    for region in self.view.sel():
      text = self.view.substr(region)
      if not text:
        sublime.status_message('Error sending to Jsfiddle: Nothing selected')
      else:
        args = {
          'html': text,
          'title': paste_title,
          'description': DESCR,
          'dtd': 'html 4',
          'wrap': 'l'
        }

        js_submit = '$(document).ready(function() {$("#form").submit(); });'

        input_field = "<input type='hidden' name='{0}' value='{1}' />"

        textarea_field = "<textarea name='{0}' style=\"display: none;\">{1}</textarea>"

        base_file_contents = \
        """
        <script src='http://www.google.com/jsapi'></script>
        <script>
          google.load('jquery', '1.3.2');
        </script>

        <script>
          {0}
        </script>

        Sending to Jsfiddle...

        <form id='form' action='{1}' method='POST' />
          {2}
        </form>
        """

        input_fields = ""

        for key, value in args.items():
          if key == 'html':
            input_fields += textarea_field.format(key, value)
          else:
            input_fields += input_field.format(key, value)

        with open('temp_file.html', 'w') as file:
          file.write(base_file_contents.format(js_submit, API_URL, input_fields))
          file.close()
          webbrowser.open(os.path.abspath(file.name))
