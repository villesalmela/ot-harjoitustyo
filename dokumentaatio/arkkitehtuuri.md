# Arkkitehtuuri
## Yleiskuva
![Arkkitehtuuri](arkkitehtuuri.png)

Yllä oleva kaavio on toteutettu oheisessa d2-koodilla.
```d2
# SHARED PROPERTIES
direction: up
classes: {
  package: {
    shape: package
    label.near: outside-top-left
    style.font-size: 28
  }
  dependency: {
    style.stroke-dash: 3
    target-arrowhead: {
      shape: arrow
    }
  }
  implementation: {
    style.stroke-dash: 3
    target-arrowhead: {
      shape: triangle
      style.filled: false
    }
  }
  composition: {
    target-arrowhead: {
      shape: diamond
      style.filled: true
    }
  }
  aggregation: {
    target-arrowhead: {
      shape: diamond
      style.filled: false
    }
  }
  enum: {
    style.fill: "#0047AB"
    shape: class
  }
  abstract: {
    style.fill: "#C04000"
    shape: class
  }
  "class": {
    shape: class
  }
}

# Objects
ui: {
  class: package
  PcapUi: {
    class: class
  }
}
analyzer: {
  class: package
  DNSAnalyzer: {
    class: class
  }
}
packet_parser: {
  class: package
  PcapParser: {
    class: class
  }
  DNSParser: {
    class: class
  }
  DHCPParser: {
    class: class
  }
  PcapParser -> DNSParser: {
    class: dependency
  }
  PcapParser -> DHCPParser: {
    class: dependency
  }
}
components: {
  class: package
  Layer: {
    class: class
  }
  Packet: {
    class: class
  }
  Layer -> Packet: {
    class: composition
  }
}
\"layers": {
  LayerLevel -> LayerConfig: {
    class: composition
  }
  Properties -> LayerConfig: {
    class: aggregation
  }
  class: package
  LayerLevel: {
    class: enum
  }
  LayerConfig: {
    class: abstract
  }
  Ethernet: {
    class: class
  }
  IP: {
    class: class
  }
  TCP: {
    class: class
  }
  UDP: {
    class: class
  }
  DNS: {
    class: class
  }
  DHCP: {
    class: class
  }
  Ethernet -> LayerConfig: {
    class: implementation
  }
  IP -> LayerConfig: {
    class: implementation
  }
  TCP -> LayerConfig: {
    class: implementation
  }
  UDP -> LayerConfig: {
    class: implementation
  }
  DNS -> LayerConfig: {
    class: implementation
  }
  DHCP -> LayerConfig: {
    class: implementation
  }
  Properties: {
    class: package
    DNSDir: {
      class: enum
    }
    DNSOpCode: {
      class: enum
    }
    DNSQType: {
      class: enum
    }
    BOOTPOpCode: {
      class: enum
    }
    DHCPMessageType: {
      class: enum
    }
  }
}

# Inter-container links
packet_parser -> components: {
  class: dependency
}
analyzer -> components: {
  class: dependency
}
\"layers".LayerConfig -> components.Layer: {
  class: composition
}
packet_parser -- ui -- analyzer

# Explaining colors
Legend: {
  Abstract: {
    class: abstract
  }
  Enum: {
    class: enum
  }
  \"Class": {
    class: class
  }
  style.fill: "#FFFAF0"
}
```
## Sekvenssikaavio
Oheinen kaavio esittää ylätasolla, miten tapahtuu PCAP-tiedoston valinta, parsinta, analysointi ja
visualisoinnin konfigurointi.
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant Main
  participant Parser
  participant Analyzer
  User->>UI: Select file
  UI->>Main: process_file("capture.pcap")
  Main->>Parser: parse_pcap("capture.pcap")
  Parser-->>Main: parsed_packets
  Main->>Analyzer: analyze(parsed_packets)
  Analyzer-->>Main: data
  Main-->>UI: figure_configuration
  UI-->>User: View figure
```