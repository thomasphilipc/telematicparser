from folium import FeatureGroup,Map,Marker, Icon, LatLngPopup, LayerControl
from folium.plugins import MeasureControl


def test_unit():

    feature_group = FeatureGroup(name='Teltonika')



    m = Map(
        location=[25.09841,55.16275],
        zoom_start=2,
        tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoidGFsazJ0cGMiLCJhIjoiY2ptenozdm0yMWlyNTNwcGhwbzc3dG9rNCJ9.NzVTxRk8eVz6g_BrbjonWg',
        attr='Mapbox'
    )

    Marker(
        location=[25.09955,55.16263],
        popup='Mt. Hood Meadows',
        icon=Icon(icon='dashboard')
    ).add_to(feature_group)



    Marker(
        location=[25.10124,55.16332],
        popup='Timberline Lodge',
        icon=Icon(color='green')
    ).add_to(feature_group)

    Marker(
        location=[25.10255,55.16545],
        popup='''<p>Asset Name: Teltonika</p>
<p><img src="https://html-online.com/editor/tinymce4_6_5/plugins/emoticons/img/smiley-cool.gif" alt="cool" /></p>
<p>Speed: <span style="color: #ff0000;">12 km/hr</span></p>
<p>&nbsp;</p>
<p>&nbsp;</p>''',
        icon=Icon(color='red', icon='screenshot')
    ).add_to(feature_group)

    m.add_child(LatLngPopup())

    feature_group.add_to(m)

    LayerControl().add_to(m)

    m.add_child(MeasureControl())

    m.save('osm.html')


if __name__ == '__main__':
    test_unit()
