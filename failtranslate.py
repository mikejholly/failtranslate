import sys
import polib
import urllib
import simplejson
import re
import xml.sax.saxutils as saxutils

def translate(msgid, lang_from, lang_to):
  print msgid
  pl = ['^', '@', '*', '_']
  m = {}
  matches = re.findall('[\@|\!][a-z]+', msgid)
  for match in matches:
    r = pl[len(m)]
    msgid = msgid.replace(match, r)
    m[r] = match
  params = {'v':'1.0', 'q': msgid}
  url = "http://ajax.googleapis.com/ajax/services/language/translate?%s&langpair=%s%%7C%s" % (urllib.urlencode(params), lang_from, lang_to)
  resp = simplejson.load(urllib.urlopen(url))
  msgstr = saxutils.unescape(resp['responseData']['translatedText'])
  for k, v in m.items():
    msgstr = msgstr.replace(k, v)
  print msgstr
  print
  return msgstr

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print "Usage: %s file.po from-lang to-lang" % sys.argv[0]
    sys.exit()
  po_file = sys.argv[1]
  lang_from = sys.argv[2]
  lang_to = sys.argv[3]
  po = polib.pofile(po_file)
  for entry in po:
    if entry.msgid_plural:
      entry.msgstr_plural[0] = translate(entry.msgid, lang_from, lang_to)
      entry.msgstr_plural[1] = translate(entry.msgid_plural, lang_from, lang_to)
    else:
      entry.msgstr = translate(entry.msgid, lang_from, lang_to)
  po_out = po_file.replace('.po', '')
  po_out = '%s-%s.po' % (po_out, lang_to)
  po.save(po_out)