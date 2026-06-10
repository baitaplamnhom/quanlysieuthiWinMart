import pandas as pd


class QuanLySP:
    def __init__(self, file_path, title=[]):
        self.file_path = file_path
        self.title = title

    def list(self, page, page_size):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        start = (page - 1) * page_size
        end = start + page_size

        page = {
            "page": page,
            "page_size": page_size,
            "total_records": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
            "data": [data.iloc[i].to_dict()
                     for i in range(start, min(end, len(data)))]
        }

        return page

    def search(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        result = data[
            data[title_keyword]
            .astype(str)
            .str.contains(str(keyword), case=False, na=False)
        ]

        return result

    def delete(self, title_keyword, keyword):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        result = data[
            data[title_keyword].astype(str) != str(keyword)
        ]

        result.to_csv(self.file_path, index=False)

        return True

    def update(self, title_keyword, keyword, title_edit=[], new_data=[]):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        # ===== Hỗ trợ cách gọi hiện tại từ giao diện =====
        if len(new_data) == 0 and len(title_edit) > 0:

            index = data[
                data[title_keyword].astype(str) == str(keyword)
            ].index

            if len(index) == 0:
                return False

            row = index[0]

            try:
                data.at[row, "ma_sp"] = str(title_edit[0])
                data.at[row, "ten_sp"] = str(title_edit[1])
                data.at[row, "gia"] = int(float(title_edit[2]))
                data.at[row, "don_vi"] = str(title_edit[3])
                data.at[row, "so_luong"] = int(float(title_edit[4]))

                data.to_csv(self.file_path, index=False)

                return True

            except Exception as e:
                print("Lỗi cập nhật:", e)
                return False

        # ===== Chức năng cũ =====
        try:
            for i in title_edit:
                data.loc[
                    data[title_keyword].astype(str) == str(keyword),
                    i
                ] = new_data[title_edit.index(i)]

            data.to_csv(self.file_path, index=False)

            return True

        except Exception as e:
            print("Lỗi cập nhật:", e)
            return False

    def create(self, new_data):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        new_row = pd.DataFrame(
            [new_data],
            columns=self.title
        )

        data = pd.concat(
            [data, new_row],
            ignore_index=True
        )

        data.to_csv(self.file_path, index=False)

        return True

    def max(self, title_keyword):
        data = pd.read_csv(self.file_path)

        if self.title:
            data = data[self.title]

        max_value = data[title_keyword].max()

        return max_value