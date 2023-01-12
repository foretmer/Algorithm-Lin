from assistant import RotationType, Axis, intersect, set_to_decimal

DEFAULT_DECIMALS = 2
START_POSITION = [0, 0, 0]


class Item:
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.rotation_type = 0
        self.position = START_POSITION
        self.decimals = DEFAULT_DECIMALS

    def format_numbers(self, decimals):
        self.length = set_to_decimal(self.length, decimals)
        self.width = set_to_decimal(self.width, decimals)
        self.height = set_to_decimal(self.height, decimals)
        self.decimals = decimals

    def string(self):
        return "%s(%s x %s x %s = %s) position is %s  rotation is %s" % (
            self.name, self.length, self.width, self.height,self.get_volume(),
            self.position, self.rotation_type
        )

    def get_volume(self):
        return set_to_decimal(
            self.length * self.width * self.height, self.decimals
        )


    def get_size(self):
        if self.rotation_type == RotationType.LWH:
            size = [self.length, self.width, self.height]
        elif self.rotation_type == RotationType.WHL:
            size = [self.width, self.height, self.length]
        elif self.rotation_type == RotationType.WLH:
            size = [self.width, self.length, self.height]
        elif self.rotation_type == RotationType.HLW:
            size = [self.height, self.length, self.width]
        elif self.rotation_type == RotationType.HWL:
            size = [self.height, self.width, self.length]
        elif self.rotation_type == RotationType.LHW:
            size = [self.length, self.height, self.width]
        else:
            size = []

        return size


class Bin:
    def __init__(self, name, length, width, height):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.fitted_items = []
        self.unfitted_items = []
        self.decimals = DEFAULT_DECIMALS

    def format_numbers(self, decimals):
        self.length = set_to_decimal(self.length, decimals)
        self.width = set_to_decimal(self.width, decimals)
        self.height = set_to_decimal(self.height, decimals)
        self.decimals = decimals

    def string(self):
        return "%s(%s x %s x %s = %s)" % (
            self.name, self.length, self.width, self.height,
            self.get_volume()
        )

    def get_volume(self):
        return set_to_decimal(
            self.length * self.width * self.height, self.decimals
        )

    def put_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, 6):
            item.rotation_type = i
            size = item.get_size()
            if (
                self.length < pivot[0] + size[0] or
                self.width < pivot[1] + size[1] or
                self.height < pivot[2] + size[2]
            ):
                continue

            fit = True

            for current_item in self.fitted_items:
                if intersect(current_item, item):
                    fit = False
                    break

            if fit:
                self.fitted_items.append(item)

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit


class Packer:
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)

    def pack_to_bin(self, bin, item):
        fitted = False

        if not bin.fitted_items:
            response = bin.put_item(item, START_POSITION)

            if not response:
                bin.unfitted_items.append(item)

            return

        for axis in range(0, 3):
            items_in_bin = bin.fitted_items

            for ib in items_in_bin:
                # pivot = [0, 0, 0]
                w, h, d = ib.get_size()
                if axis == Axis.LENGTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]

                if bin.put_item(item, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            bin.unfitted_items.append(item)

    def pack(
        self, distribute_items=False,
        decimals=DEFAULT_DECIMALS
    ):
        for bin in self.bins:
            bin.format_numbers(decimals)

        for item in self.items:
            item.format_numbers(decimals)

        self.bins.sort(
            key=lambda bin: bin.get_volume(), reverse=True
        )
        self.items.sort(
            key=lambda item: item.get_volume(), reverse=True
        )

        for bin in self.bins:
            for item in self.items:
                self.pack_to_bin(bin, item)


            if distribute_items:
                for item in bin.items:
                    self.items.remove(item)