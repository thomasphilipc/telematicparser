import folium


def test_unit():
    m = folium.Map(
        location=[25.09841,55.16275],
        zoom_start=12
       # tiles='Stamen Terrain'
    )

    folium.Marker(
        location=[25.09955,55.16263],
        popup='Mt. Hood Meadows',
        icon=folium.Icon(icon='dashboard')
    ).add_to(m)

    folium.Marker(
        location=[25.10124,55.16332],
        popup='Timberline Lodge',
        icon=folium.Icon(color='green')
    ).add_to(m)

    folium.Marker(
        location=[25.10255,55.16545],
        popup='''<p>Asset Name: Teltonika</p>
<p><img src="https://html-online.com/editor/tinymce4_6_5/plugins/emoticons/img/smiley-cool.gif" alt="cool" /></p>
<p>Speed: <span style="color: #ff0000;">12 km/hr</span></p>
<p>&nbsp;</p>
<p>&nbsp;</p>''',
        icon=folium.Icon(color='red', icon='screenshot')
    ).add_to(m)

    m.add_child(folium.LatLngPopup())

    m.save('osm.html')


if __name__ == '__main__':
    test_unit()
