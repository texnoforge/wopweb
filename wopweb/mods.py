from texnomagic.mods import get_online_mods


def download_all_mods():
	print("downloading all Words of Power mods...")
	all_mods = get_online_mods()
	for m in all_mods:
		print("  DOWNLOADING %s" % m)
