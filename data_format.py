class DataFormat:
    Latitude: str
    Longitude: str
    Altitude: str
    CaptureTime: str
    Roll: float
    Pitch: float
    Heading: float
    SequenceUUID: str
    Orientation: int
    DeviceMake: str = "sony"
    DeviceModel: str = "Ladybug"
    ImageSize: str = "8192x4096"
    FoV: str = "360"
    PhotoUUID: str
    image_name: str
    image_path: str


class CsvFormat:
    OutputFileName: str = 'csv_out'
