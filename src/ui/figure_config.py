class FigureConfig:

    def __init__(
            self,
            title,
            data1,
            xlabel,
            y1label,
            color1,
            data2=None,
            y2label=None,
            color2=None) -> None:
        self.title = title
        self.data1 = data1
        self.xlabel = xlabel
        self.y1label = y1label
        self.color1 = color1
        self.data2 = data2
        self.y2label = y2label
        self.color2 = color2
