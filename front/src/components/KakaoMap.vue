<template>
  <div>
    <h1 class="ercword">주변 은행 검색</h1>
    <div class="container custom-border">
      <div id="map" class="map"></div>
      <div id="menu_wrap" class="bg_white">
        <div class="option">
          <div>
            <!-- 드롭다운 형식으로 변경된 부분 -->
            <select id="keyword" class="custom-border">
              <option value="">은행 선택</option>
              <option value="우리은행">우리은행</option>
              <option value="신한은행">신한은행</option>
              <option value="하나은행">하나은행</option>
            </select>
            <!-- 지역 입력은 그대로 유지 -->
            <input type="text" id="region" size="15" placeholder="지역 입력" class="custom-border" />
            <!-- 검색 버튼 -->
            <button @click="searchPlaces" class="custom-border">검색하기</button>
          </div>
        </div>
        <ul id="placesList"></ul>
        <div id="pagination"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initMap();
    } else {
      this.addKakaoMapScript();
    }
  },
  methods: {
    addKakaoMapScript() {
      const script = document.createElement("script");
      script.onload = () => kakao.maps.load(this.initMap);
      script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&libraries=services`
      document.head.appendChild(script);
    },
    initMap() {
      navigator.geolocation.getCurrentPosition(position => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const mapContainer = document.getElementById("map");
        const mapOption = {
          center: new kakao.maps.LatLng(latitude, longitude),
          level: 3,
        };

        this.map = new kakao.maps.Map(mapContainer, mapOption);
        this.ps = new kakao.maps.services.Places();
        this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
        this.markers = [];
      });
    },
    searchPlaces() {
      const keyword = document.getElementById("keyword").value.trim();
      const region = document.getElementById("region").value.trim(); // 지역 입력 값 가져오기

      if (!keyword || !region) {
        alert("키워드와 지역을 모두 입력해주세요!");
        return;
      }

      const query = keyword + ' ' + region; // 지역 정보를 키워드와 합침

      this.ps.keywordSearch(query, this.placesSearchCB.bind(this)); // 합친 쿼리로 검색 수행
    },
    placesSearchCB(data, status, pagination) {
      if (status === kakao.maps.services.Status.OK) {
        this.displayPlaces(data);
        this.displayPagination(pagination);
      } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        alert("검색 결과가 존재하지 않습니다.");
      } else if (status === kakao.maps.services.Status.ERROR) {
        alert("검색 결과 중 오류가 발생했습니다.");
      }
    },
    displayPlaces(places) {
      const listEl = document.getElementById("placesList");
      const bounds = new kakao.maps.LatLngBounds();

      this.removeAllChildNodes(listEl);
      this.removeMarker();

      places.forEach((place, i) => {
        const placePosition = new kakao.maps.LatLng(place.y, place.x);
        const marker = this.addMarker(placePosition, i);
        const itemEl = this.getListItem(i, place);

        bounds.extend(placePosition);

        kakao.maps.event.addListener(marker, "mouseover", () => {
          this.displayInfowindow(marker, place.place_name);
        });

        kakao.maps.event.addListener(marker, "mouseout", () => {
          this.infowindow.close();
        });

        itemEl.onmouseover = () => {
          this.displayInfowindow(marker, place.place_name);
          itemEl.style.backgroundColor = "#f0f8ff"; // 항목에 마우스를 올렸을 때 배경색 변경
        };

        itemEl.onmouseout = () => {
          this.infowindow.close();
          itemEl.style.backgroundColor = ""; // 마우스를 뗐을 때 배경색 초기화
        };

        itemEl.onclick = () => {
          this.map.setCenter(placePosition);
          this.map.setLevel(3);
          this.displayInfowindow(marker, place.place_name);
        };

        listEl.appendChild(itemEl);
      });

      this.map.setBounds(bounds);
    },
    getListItem(index, place) {
      const el = document.createElement("li");
      const itemStr = `
        <span class="marker_number">${index + 1}</span>
        <div class="info">
          <h5>${place.place_name}</h5>
          ${place.road_address_name ? `<span>${place.road_address_name}</span><span class="jibun gray">${place.address_name}</span>` : `<span>${place.address_name}</span>`}
          <span class="tel">${place.phone}</span>
        </div>
      `;
      el.innerHTML = itemStr;
      el.className = "item";
      return el;
    },
    addMarker(position, idx) {
      const imageSrc = `https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png`;
      const imageSize = new kakao.maps.Size(36, 37);
      const imgOptions = {
        spriteSize: new kakao.maps.Size(36, 691),
        spriteOrigin: new kakao.maps.Point(0, idx * 46 + 10),
        offset: new kakao.maps.Point(13, 37),
      };
      const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
      const marker = new kakao.maps.Marker({
        position: position,
        image: markerImage,
      });

      marker.setMap(this.map);
      this.markers.push(marker);

      return marker;
    },
    removeMarker() {
      this.markers.forEach((marker) => marker.setMap(null));
      this.markers = [];
    },
    displayPagination(pagination) {
      const paginationEl = document.getElementById("pagination");

      this.removeAllChildNodes(paginationEl);

      for (let i = 1; i <= pagination.last; i++) {
        const el = document.createElement("a");
        el.href = "#";
        el.innerHTML = i;
        el.className = pagination.current === i ? "on" : "";
        el.onclick = () => {
          pagination.gotoPage(i);
        };
        paginationEl.appendChild(el);
      }
    },
    displayInfowindow(marker, title) {
      const content = `<div style="padding:5px;z-index:1;">${title}</div>`;
      this.infowindow.setContent(content);
      this.infowindow.open(this.map, marker);
    },
    removeAllChildNodes(el) {
      while (el.hasChildNodes()) {
        el.removeChild(el.lastChild);
      }
    },
  },
};
</script>

<style>
.container {
  display: flex;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1); /* Adding shadow */
}
.map {
  width: 70%;
  height: 600px;
}
.bg_white {
  width: 30%;
  background: white;
  overflow-y: auto;
  height: 600px;
  border-radius: 8px; /* Border-radius for the side panel */
}
.option {
  padding: 10px 10px 0;
}
#placesList {
  list-style-type: none; /* Remove dots from the list */
  padding: 0;
  margin: 0;
}
#placesList .item {
  padding: 10px;
  border-bottom: 1px solid #e2e2e2;
  cursor: pointer; /* Cursor changes to pointer on hover */
}
#placesList .item:hover {
  background-color: #f0f8ff; /* Change background color on hover */
}
#pagination a {
  margin: 0 2px;
  padding: 3px 6px;
  border: 1px solid #e2e2e2;
  color: #333;
  text-decoration: none;
  cursor: pointer;
  border-radius: 5px; /* Rounded corners for pagination buttons */
}
#pagination a.on {
  border-color: #1675F2; /* Changing the 'on' state border color */
  color: #007bff;
}

.ercword {
  color: #333;
}

.custom-border {
  border: 1px solid #1675F2; /* Thinner border and changing border color */
  margin: 2px;
  border-radius: 5px; /* Rounded corners adjusted for all elements with custom-border */
}

input[type="text"], button, select {
  border-radius: 5px; /* Rounded corners for input fields, buttons, and dropdowns */
}

.marker_number {
  font-weight: bold;
  color: #1675F2; /* Changing the marker number color */
  display: inline-block;
  width: 20px; /* Fixed width for alignment */
}
</style>
