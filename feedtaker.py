#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gtk, pygtk, webkit
from gtk import UIManager

from gettext import gettext as _
import gettext, feedparser, time

test_addr='https://www.lostfilm.tv/rss.xml'

class NewsWindow:
	def onSelectionChanged(self, tree_selection, i=0, b=0):
		#print "shot!"
		(model, pathlist) = tree_selection.get_selected()
		for path in pathlist :
			print path
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			print value

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(640, 480)
		#~ self.window.set_position(gtk.WINDOW_POS_CENTER_ALWAYS)
		self.window.connect("destroy", self.destroy)

		self.vbox = gtk.VBox(False, 8)

		#~ mb = gtk.MenuBar()
		#~ newl=gtk.MenuItem('New')
		#~ exiti=gtk.MenuItem('Quit')
		#~ exiti.connect('activate', quit)
		#~ mb.append(newl)
		#~ mb.append(exiti)
		#~ mb.show_all()
		acts=[
			("fnew", gtk.STOCK_NEW, _("New"), None, None, self.fnew),
			("fquit", gtk.STOCK_QUIT, _("Exit"), None, None, quit),
			('File', None, '_File'),
			('Mute', None, '_Mute'),
			('AM', None, '_AM'), 
			('FM', None, '_FM'),#('FM', None, '_FM', '<Control>f', 'FM Radio', 1),
			('SSB', None, '_SSB'),
			('RadioBand', None, '_RadioBand'),
		]
		
		propxml="""
			<ui>
			<menubar name='MB'>
				<menu action='File'>
					<menuitem  action="fnew" />
					<menuitem  action="fquit" />
				</menu>
				<menu action="RadioBand">
				<menuitem action="AM"/>
		<menuitem action="FM"/>
		<menuitem action="SSB"/>
		</menu>
				</menubar>
				
				<toolbar name="TB">
					<toolitem action='fnew' />
					<toolitem action="fquit"/>
					<separator/>
					<toolitem action="Mute"/>
					<separator name="sep1"/>
					<placeholder name="RadioBandItems">
						<toolitem action="AM"/>
						<toolitem action="FM"/>
						<toolitem action="SSB"/>
					</placeholder>
				</toolbar>
			</ui>
			"""
		ag=gtk.ActionGroup("fr_ag")
		ag.add_actions(acts, None)
		uimanager=gtk.UIManager()
		uimanager.insert_action_group(ag, 0)
		uimanager.add_ui_from_string(propxml)
		mb = uimanager.get_widget('/MB')
		tb=uimanager.get_widget('/TB')
		tb.set_icon_size(gtk.ICON_SIZE_MENU)
		#~ print mb, tb, ag
		
		#~ self.vbox.pack_start(mb, False, False,0)

		self.sw2=gtk.ScrolledWindow()
		self.treeView = gtk.TreeView()
		self.treeView.set_rules_hint(True)
		self.create_columns(self.treeView)
		self.sw2.add(self.treeView)
		#self.update_list()
		self.vbox.pack_start(mb, False)
		self.vbox.pack_start(tb, False)
		
		self.vbox.pack_start(self.sw2, True)

		#~ self.sw = gtk.ScrolledWindow()
		#~ self.sw.set_shadow_type(gtk.ShadowType.ETCHED_IN)
		#~ self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)		
		#~ self.vview = webkit.WebView()
		#~ self.sw.add(self.vview)
		#~ self.vbox.pack_start(self.sw, True)
		
		# add the TreeView to the scrolled window
		#self.sw.add(self.treeView)
		self.statusbar = gtk.Statusbar()
		self.vbox.pack_end(self.statusbar, False)
		self.window.add(self.vbox)

		self.store=gtk.ListStore(str, str, str)
		#~ self.store.append(['','',''])
		self.treeView.set_model(self.store)
		self.fparse(test_addr)
		self.window.show_all()
		
		"""posts = sq.execute(str('select id, title, post_url from posts where feed_url=? and read == \'false\' limit %i' % itemsperfeed), (feed[2],))
		if len(posts) > 0:
					posts.reverse()
					submenu.append(Gtk.SeparatorMenuItem())
				
					for post in posts:
						menu_row = self.create_menu_item(post[1], post[0], post[2])
						submenu.append(menu_row)
		if not url == '':
			posts = sq.execute('select id, title, post_url from posts where feed_url=? and read=\'false\'', (url,))
			if len(posts)>0:
				posts.reverse()
				for post in posts:
					print post
					#if len(post[0])>0:
					store.append([post[1], post[0], post[2]])
					sleep(0.6)
		else:
			feeds = sq.execute('select feed_url from feeds')

			for feed in feeds:
				posts = sq.execute('select id, title, post_url from posts where feed_url=? and read=\'false\'', feed)
				if len(posts)>0:
					posts.reverse()
					for post in posts:
						print post
						if len(post[0])>0:
							store.append(post[1], post[0], post[2])
						sleep(0.6)

				#sq.execute('update posts set read=\'true\' where feed_url=?', feed)		
		sq.commit()
		sq.close()
		self.treeView.set_model(store)
		#self.treeView.row_activated.connect(onSelectionChanged)
		self.sel=self.treeView.get_selection()
		self.sel.connect('changed', onSelectionChanged, self.sel)"""

	def create_columns(self, treeView):
		"""create the columns """
        # CellRendererText = an object that renders text into a Gtk.TreeView cell
		rendererText1 = gtk.CellRendererText()
        # column = a visible column in a Gtk.TreeView widget
        # param: title, cell_renderer, zero or more attribute=column pairs
        # text = 0 -> attribute values for the cell renderer from column 0 in the treemodel
		column1 = gtk.TreeViewColumn("Date", rendererText1, text=0)
        # the logical column ID of the model to sort
		column1.set_sort_column_id(0)
        # append the column
		treeView.append_column(column1)
 
		rendererText2 = gtk.CellRendererText()
		column2 = gtk.TreeViewColumn("Title", rendererText2, text=1)
		column2.set_sort_column_id(1)    
		treeView.append_column(column2)
 
		treeView.set_headers_clickable(True)


	def destroy(self, widget, data=None):
		gtk.main_quit()
		return False

	def fnew(self, e):
		pass
		
	def fparse(s, uri):
		s.store.clear()
		feed = feedparser.parse(uri)
		for i in feed['items']:
			#~ '%a %b %d %H:%M:%S %Y'
			td= time.strftime('%Y-%m-%d %a, %H:%M', i['published_parsed'])
			#~ print time.strptime(i['published_parsed']), time.strptime(i['published'])
			s.store.append([td, i['title'], ''])
			#~ s.store.append([i['title_detail']['value'], '', ''])
			#~ print i['title_detail']['value'], i['links'][0]

if __name__ == '__main__':
	n=NewsWindow()
	gtk.main()
